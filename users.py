# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

sa.__version__

engine = create_engine('sqlite:///users.db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
                            self.name, self.fullname, self.password)
      
User.__table__

Base.metadata.create_all(engine)

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
ed_user.name
ed_user.password
print(ed_user.id)

Session = sessionmaker(bind=engine)

session = Session()
session.add(ed_user)
our_user = session.query(User).filter_by(name='ed').first() 

session.commit()


