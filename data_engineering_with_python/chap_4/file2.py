import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

results=session.query(User).all()

for row in results[:5]:
    print(f'Name:\t{row.name}, ID:\t{row.id}, Street:\t{row.street}, City:\t{row.city}, Zip:\t{row.zip}')
    
# inspector=sqlalchemy.inspect(engine)


# table = 'users'
# columns = ['name','street','city','zip']

# fake=Faker()

# rows=[]

# for i in range(1000):
#     u=User(name=fake.name(),street=fake.street_address(),city=fake.city(),zip=fake.zipcode())
#     rows.append(u)

# session.add_all(rows)
# print(rows[1])
# x=session.commit()
# print(x)