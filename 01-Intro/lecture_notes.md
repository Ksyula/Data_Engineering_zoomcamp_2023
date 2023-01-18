# Lesson 1
docker run hello-world
docker run  --help
docker run -it ubuntu bash
docker run -it python:3.9 bash

docker build --help
docker build -t test:pandas .
docker run -it test:pandas
docker run -it test:pandas 2021-01-15

# Lesson 2
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
postgres:13

pip install pgcli

