#!/bin/bash

URL="https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
  ingest_data_zone.py \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=zones \
  --url="$URL"
