from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__= 'users'
    name=Column(String)
    id=Column(Integer, primary_key=True)
    street=Column(String)
    city=Column(String)
    zip=Column(String)
    
    
