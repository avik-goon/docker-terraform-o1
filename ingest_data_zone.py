#!/usr/bin/env python
# coding: utf-8

import os
import shutil

import pandas as pd
from time import time
from sqlalchemy import create_engine
import  argparse


def ingest_data_zone(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # File names
    csv_file = "data.csv"

    # Download the csv file
    os.system(f"wget {url} -O {csv_file}")

  
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000,
                          dtype={"store_and_fwd_flag": str})

    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    for df in df_iter:
        t_start_time = time()
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
    ingest_data_zone(args)









