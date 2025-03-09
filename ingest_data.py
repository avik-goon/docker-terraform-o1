#!/usr/bin/env python
# coding: utf-8
import gzip
import os
import shutil

import pandas as pd
from time import time
from sqlalchemy import create_engine
import  argparse


def ingest_data(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # File names
    gz_file = "data.csv.gz"
    csv_file = "data.csv"

    # Download the gzip file
    os.system(f"wget {url} -O {gz_file}")

    # Extract the gzip file
    with gzip.open(gz_file, 'rb') as f_in, open(csv_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000,
                          dtype={"store_and_fwd_flag": str})

    # df = next(df_iter)
    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    #
    # df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    for df in df_iter:
        t_start_time = time()
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df["store_and_fwd_flag"] = df["store_and_fwd_flag"].astype(str)
        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end_time = time()
        print('Inserted another chunk, took %.2f seconds' % (t_end_time - t_start_time))





if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        prog='Pipeline',
                        description='Ingest CSV data to Postgres')

    # user
    # password
    # host
    # port
    # db name
    # table name
    # csv url

    parser.add_argument('--user', help='postgres username')
    parser.add_argument('--password', help='postgres password')
    parser.add_argument('--host', help='postgres host url')
    parser.add_argument('--port', help='postgres port url')
    parser.add_argument('--db', help='postgres database name')
    parser.add_argument('--table_name', help='postgres table name')
    parser.add_argument('--url', help='csv file location')


    args = parser.parse_args()
    ingest_data(args)









