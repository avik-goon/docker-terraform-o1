#container_name: taxi_ingest:v001
FROM python:3.12.3

RUN apt update && apt install -y wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY ingest_data.py ingest_data.py
COPY ingest_data_zone.py ingest_data_zone.py 


ENTRYPOINT ["python"]

