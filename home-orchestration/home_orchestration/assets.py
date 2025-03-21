from dagster import EnvVar, asset, AssetExecutionContext
import sqlite3
from io import BytesIO
from minio import Minio
import requests
import os
import json
import csv
from .util import CSVFileMapper, FieldMapper
# from ..partitions import monthly_partition


# ====================================================================================
@asset
def vocab_csv():
    SOURCE_PATH = '/home/bernd/Courses/cesky/czech_vocabs_wide.csv' #EnvVar("VOCAB_CSV_SOURCE")
    
    # Create the client
    client = Minio(
        endpoint="localhost:9000",
        access_key="myminioadmin",
        secret_key="myminioadmin",
        secure=False
        )
    
    # Read the CSV file.
    with open(SOURCE_PATH, newline='') as csvfile:
        lines = list(csvfile)
    
    del lines[0]
    
    binary_buffer = BytesIO()

    binary_buffer.write(lines)
    binary_buffer.seek(0)
    
    # Put the object into minio
    client.put_object(
        bucket_name="dagster-orchestrator",
        prefix='learning-app/',
        object_name="czech_vocabs_wide.csv", 
        data=binary_buffer
        )
    

# ====================================================================================
@asset()
def vocab_database() -> None:
    SOURCE_PATH = EnvVar("VOCAB_CSV_SOURCE")
    DATA_BASE = EnvVar("LEARNING_APP_DB")
    TABLE_NAME = EnvVar("LEARNING_APP_TABLE_NAME")
    
    csv_map = CSVFileMapper(
        name=SOURCE_PATH,
        columns=['id', 'left', 'right', 'info_left', 'info_right', 'tag_subject'],
        json_columns=FieldMapper(
            name='tags',
            columns=[
                'tag_info', 
                'tag_src', 
                'tag_type', 
                'tag_1', 
                'tag_2', 
                'tag_3', 
                'tag_4', 
                'tag_5'
                ]
            )
        )
    
    con = sqlite3.connect(DATA_BASE)
    cur = con.cursor()

    with open(csv_map.name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=csv_map.source_column_names, delimiter=';')
        # create tuples:
        data_to_db = []
        for row in reader:
            # dumps tag columns into list
            tag_col = json.dumps({csv_map.json_columns.name: [row[item] for item in csv_map.json_columns.columns if row[item] != ""]})
            
            # normal columns:
            data_row = [row[item] for item in csv_map.columns]
            
            # append together
            data_row.append(tag_col)
            data_to_db.append(tuple(data_row))
            
    print(data_to_db[0])      
    number_table_columns = len(csv_map.columns) + 1
    column_name_string = '(' + ','.join(csv_map.target_column_names) + ')'
    value_string = '(' + ','.join(['?' for k in range(number_table_columns)]) + ')'        
    insert_string = f"INSERT INTO {TABLE_NAME} {column_name_string} VALUES {value_string};"
    print(insert_string)
    cur.executemany(insert_string, data_to_db)
    con.commit()
    con.close()


