#!/usr/bin/env python
# coding: utf-8

# # Final Project Notebook - Part 2

import pandas
import pandas as pd
import json
import pandas.io.json as pd_json
import sqlalchemy
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from IPython import get_ipython

import warnings
warnings.filterwarnings('ignore')

import random
import time
from getpass import getpass
from pandas import read_sql
import datetime
import matplotlib.pyplot as plt
from pandas import DataFrame
from google.cloud import storage
import psycopg2
from sqlalchemy.orm import sessionmaker


# ### 1. Pull data from analytical data store (your bucket) and aggregate into tabular format. 

bucket_name = 'reddit-data-bucket-jdxqd-2'
source_blob_name = 'analytics -20210306-003321' #Note: If pulling this automatically, make this the most recent (highest number)
destination_file_name = 'analytics -20210306-003321'

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )
    
download_blob(bucket_name, source_blob_name, destination_file_name)

# Convert the txt file to a dataframe suitable for your SQL database
df = pd.read_json(destination_file_name)

with open(destination_file_name) as data_file:    
    data = json.load(data_file)  

df = pd_json.json_normalize(data, 'entities', errors='ignore')

# Rename columns
df.rename({'sentiment.magnitude': 'sentiment_magnitude', 'sentiment.score': 'sentiment_score'}, axis=1, inplace=True)

# Remove columns that you won't sent to SQL: 'mentions', 'type', 'metadata.mid', 'metadata.wikipedia_url'
df.drop(['mentions', 'type', 'metadata.mid', 'metadata.wikipedia_url'], axis=1, inplace=True)
#df.head()



# ### 2. Export to SQL

# initialize SQL engine
engine = create_engine('postgres://postgres:1helse1@104.198.189.65/reddit_table')
print (engine.table_names())

df.to_sql("reddit_analysis", con=engine, if_exists='append', index=False)


# ### 3. Generate one or more data visualizations

graph1 = engine.execute(" SELECT * FROM reddit_analysis ")

df = DataFrame(graph1.fetchall())
df.columns = graph1.keys()
df.head()


plt.style.use('fivethirtyeight')
df.plot.scatter(x='sentiment_score', y='sentiment_magnitude', title="Cryptocurrency Sentiment Analysis - New Reddit Posts");
plt.xlabel='Score'
plt.ylabel='Magnitude'

plt.show()


# Close SQL Connection
session = sessionmaker(bind=engine)()
session.close()
