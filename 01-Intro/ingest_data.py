#!/usr/bin/env python
# coding: utf-8

import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name # green_taxi_data
    url = params.url # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}') 

    print(f'Download the data from URL...')
    df_iter = pd.read_csv(url, compression = "gzip", iterator = True, chunksize = 100000)

    df = next(df_iter)

    df[["lpep_pickup_datetime",
    "lpep_dropoff_datetime"]] = df[["lpep_pickup_datetime", 
                                    "lpep_dropoff_datetime"]].apply(pd.to_datetime)
    # push table headers
    print(f'Push table column names to DB')
    df.head(0).to_sql(name = table_name, # Name of SQL table
          con = engine,
          if_exists = 'replace' # if table with this name exists then DROP and CREATE
         )
    # push the first chunk
    df.to_sql(name = table_name, con = engine, if_exists = 'append')
    # push the rest
    while True: #infinite loop
        try:
            t_start = time()
            # read chunk
            df = next(df_iter)
            # convert timestamp to datetime
            df[["lpep_pickup_datetime",
            "lpep_dropoff_datetime"]] = df[["lpep_pickup_datetime", 
                                            "lpep_dropoff_datetime"]].apply(pd.to_datetime)
            # push to DB
            df.to_sql(name = table_name, con = engine, if_exists = 'append')
            
            t_end = time()
            
            print(f'inserted another chunk, took {t_end - t_start} seconds')
        except StopIteration:
            print("Finished ingesting data into the posrgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='User name for postgres')
    parser.add_argument('--password', help='Password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='Database for postgres')
    parser.add_argument('--table_name', help='Table name to write the result')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)


