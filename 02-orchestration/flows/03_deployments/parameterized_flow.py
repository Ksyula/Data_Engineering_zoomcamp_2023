from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3, cache_key_fn = task_input_hash,
      cache_expiration=timedelta(days=1))
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    # df["passenger_count"].fillna(0, inplace=True)
    # print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task(log_prints=True)
def write_bq(path: Path) -> None:
    """Write DataFrame to BiqQuery"""

    df = pd.read_parquet(path)
    print(f"rows: {len(df)}")
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table="trips_data_all.yellow_taxi",
        project_id="snappy-cosine-375820",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )

@flow()
def etl_gcs_to_bq(year: int, month: int, color: str):
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(color, year, month)
    write_bq(path)

@flow()
def etl_parent_flow(months: list[int] = [2, 3],
                    year: int = 2019,
                    color: str = 'yellow'):
    for month in months:
        etl_gcs_to_bq(year, month, color)

if __name__ == "__main__":
    color = "yellow"
    year = 2019
    months = [2, 3]
    etl_parent_flow(months, year, color)