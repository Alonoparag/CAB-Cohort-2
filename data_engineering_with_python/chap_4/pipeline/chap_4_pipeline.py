from airflow import DAG, PythonOperator
from elasticsearch import helpers, Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user_schema import User

import pandas as pd
import datetime as dt
from datetime import timedelta


def get_users_from_postgres():
    db_usr='test'
    psswrd='test'
    dbname='data_eng'

    engine=create_engine(f'postgresql://{db_usr}:{psswrd}@localhost/{dbname}')
    connection=engine.connect()
    
    df=pd.read_sql('select * from users', connection=connection)
    df.to_csv('users.csv', index=False)
    connection.close()
    
def insert_users_to_es():
    es=Elasticsearch()
    df=pd.read_csv('users.csv')
    actions=[{"_index":'users_pipe',
              "_type":'doc',
              '_source':{
                  'name':row['name'],
                  'city':row['city'],
                  'zip':row['zip']
              }} for ind,row in df.iterrows()]
    res=helpers.bulk(es,actions)
    print(*res,sep='\n')
    

default_args={
    'owner':'Alon Paragu',
    'start_date':dt.datetime.today()-dt.timedelta(days=1),
    'retries':1,
    'retry_delay':dt.timedelta(minutes=5)
}

with DAG('postgres_to_elasticsearch',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),
         ) as dag:
    
    postgres_to_csv=PythonOperator(task_id='postgres_to_csv',
                                   python_callable=get_users_from_postgres)
    
    
    csv_to_elastic=PythonOperator(task_id='csv_to_elastic',
                                  python_callable=insert_users_to_es)
    postgres_to_csv>>csv_to_elastic