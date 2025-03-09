#container_name: taxi_ingest:v001
FROM python:3.12.3

RUN apt install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
