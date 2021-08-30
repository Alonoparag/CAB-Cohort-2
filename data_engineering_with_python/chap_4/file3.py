import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import elasticsearch
from elasticsearch import helpers, Elasticsearch
from faker import Faker
import pandas as pd

db_usr='test'
psswrd='test'
dbname='data_eng'

engine=sqlalchemy.create_engine(f'postgresql://{db_usr}:{psswrd}@localhost/{dbname}')
connection=engine.connect()

Base = declarative_base()

class User(Base):
    __tablename__= 'users'
    name=Column(String)
    id=Column(Integer, primary_key=True)
    street=Column(String)
    city=Column(String)
    zip=Column(String)
 

 
   
Session = sessionmaker(bind=engine)
session=Session()

postgres_results = session.query(User).all()


es = Elasticsearch()

actions = [{"_index":'users',
            '_type':'doc',
            '_souce':{
                'name':row.name,
                'street':row.street,
                'city':row.city,
                'zip':row.zip
            }} for row in postgres_results]

res=helpers.bulk(es,actions)
print(*res,sep='\n')