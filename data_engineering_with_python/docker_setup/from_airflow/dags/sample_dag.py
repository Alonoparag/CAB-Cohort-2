# # A SAMPLE DAG FILE TO CHECK THE NETWORK AND ACCESSIBILITY FOR
# # THE POSTGRES SERVER AND THE ELASTICSEARCH SERVER.
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from elasticsearch import helpers, Elasticsearch
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import datetime as dt
from datetime import timedelta


def write_to_pg(session, table):
    # Populate the POSTGRESDB with a table and data
    
    
    
    fake=Faker()
    
    for i in range(1000):
        session.add(table(name=fake.name(),city=fake.city))
    
    session.commit()
    
def transfer_from_pg_to_elasticsearch(session, table):
    #TRANSFER RECORDS FROM POSTGRESDB TO ELASTICSEARCH
    es=Elasticsearch()   
    
    results=session.query(table).all()
    actions = [{"_index":'users',
            '_type':'doc',
            '_souce':{
                'name':row.name,
                'city':row.city,
            }} for row in results]

    res=helpers.bulk(es,actions)

default_args={
    'owner':'alonparag',
    'start_date':dt.datetime.today()-dt.timedelta(days=1),
    'retries':1,
    'retry_delay':dt.timedelta(minutes=1)
}

with DAG('sample_dag',
         default_args=default_args,
         schedule_interval=timedelta(days=1),
         ) as dag:
        
        db_login={
            'db_usr':'alonparag',
            'db_psswrd':'112233445566',
            'db_name':'data_eng',
        }
        
        engine=create_engine(f'postgresql://{db_login["db_usr"]}:{db_login["db_psswrd"]}@localhost/{db_login["db_name"]}')
        connection=engine.connect()
        
        Base= declarative_base()
        
        class User(Base):
            __tablename__= 'users'
            name=Column(String)
            id=Column(Integer, primary_key=True, autoincrement=True,nullable=False)
            city=Column(String)
        
        Base.metadata.create_all(engine)
        
        Session= sessionmaker(bind=engine)
        session=Session()
        
        populate_postgress=PythonOperator(task_id='populate_postgress',
                                          callable=write_to_pg(session,User))
        
        transfer_pg_es=PythonOperator(task_id='transfer_data_from_pg_to_elasticsearch',
                                      callable=transfer_from_pg_to_elasticsearch(session, User))
        
        populate_postgress>>transfer_pg_es
        
        engine.close()
