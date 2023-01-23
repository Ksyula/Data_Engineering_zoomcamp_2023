# Lesson 1
docker run hello-world
docker run  --help
docker run -it ubuntu bash
docker run -it python:3.9 bash

docker build --help
docker build -t test:pandas .
docker run -it test:pandas
docker run -it test:pandas 2021-01-15

# Lesson 2 - dump data to Postgres DB
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
postgres:13

conda activate de-zoomcamp
pip install "psycopg[binary]" pgcli pandas

## Postges interface
pgcli -h localhost -p 5432 -u root -d ny_taxi
\dt
\d yellow_taxi_data

## Download data
NYC TLC website: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
NYC data: https://github.com/DataTalksClub/nyc-tlc-data
Data description: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
Taxi Zone Lookup Table: https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv

-- unzip .csv.gz -> .csv
find . -name '*.csv.gz' -print0 | xargs -0 -n1 gzip -d
-- work with csv in cmd
less yellow_tripdata_2021-01.csv

head -n 50 yellow_tripdata_2021-01.csv > yellow_head.csv

cat *.csv | wc -l
cat yellow_tripdata_2021-01.csv | wc -l

# Lesson 3 - pgAdmin

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
dpage/pgadmin4

### Network
docker network create pg-network

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
postgres:13

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
dpage/pgadmin4

http://localhost:8080/browser/

# Lesson 4 - pack ingest script to docker

jupyter nbconvert --to=script upload-data.ipynb

-- Dump green taxi data to DB

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_data \
  --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz

-- Check error code upon finishing (0 is good, non 0 is bad):
echo $?

docker build -t taxi_ingest:v001 .
-- run this container in the docker network

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_data \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz

python -m http.server
ifconfig
docker network ls

# Lecture 5 - docker compose

docker-compose up -d
docker-compose down
