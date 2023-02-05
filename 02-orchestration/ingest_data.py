#!/usr/bin/env python
# coding: utf-8
import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector

@task(log_prints=True, retries=1, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url: str):

    # backup files are gziped
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'green_tripdata_2020-01.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f'wget {url} -O {csv_name}')

    print(f'Download the data from URL...')
    df_iter = pd.read_csv(csv_name,
                        iterator = True, 
                        chunksize = 100000)

    df = next(df_iter)

    df[["lpep_pickup_datetime",
    "lpep_dropoff_datetime"]] = df[["lpep_pickup_datetime", 
                                    "lpep_dropoff_datetime"]].apply(pd.to_datetime)
    # push table headers
    print(f'Push table column names to DB')
    return df

@task(log_prints=True)
def transform_data(df: pd.DataFrame):
    print(f'pre: missing passenger count: {df["passenger_count"].isin([0]).sum()}')
    df = df[df['passenger_count'] != 0]
    print(f'post: missing passenger count: {df["passenger_count"].isin([0]).sum()}')
    return df

@task(log_prints=True, retries=1)
def ingest_data(table_name: str, df: pd.DataFrame):
    
    connection_block = SqlAlchemyConnector.load("postgres-connector")

    with connection_block.get_connection(begin=False) as engine:
        df.head(0).to_sql(name = table_name, # Name of SQL table
                        con = engine,
                        if_exists = 'replace' # if table with this name exists then DROP and CREATE
                            )
        # push the first chunk
        df.to_sql(name = table_name, con = engine, if_exists = 'append')
    # # push the rest
    # while True: #infinite loop
    #     try:
    #         t_start = time()
    #         # read chunk
    #         df = next(df_iter)
    #         # convert timestamp to datetime
    #         df[["lpep_pickup_datetime",
    #         "lpep_dropoff_datetime"]] = df[["lpep_pickup_datetime", 
    #                                         "lpep_dropoff_datetime"]].apply(pd.to_datetime)
    #         # push to DB
    #         df.to_sql(name = table_name, con = engine, if_exists = 'append')
            
    #         t_end = time()
            
    #         print(f'inserted another chunk, took {t_end - t_start} seconds')
    #     except StopIteration:
    #         print("Finished ingesting data into the posrgres database")
    #         break

@flow(name="Subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f'Logging Subflow for: {table_name}')

@flow(name="Ingest Flow")
def main_flow(url: str, table_name: str):

    log_subflow(table_name)
    raw_data = extract_data(url)
    data = transform_data(raw_data)
    ingest_data(table_name, data)

if __name__ == '__main__':
    main_flow("https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz",
              "green_taxi_data")


