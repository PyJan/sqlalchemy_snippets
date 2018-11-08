#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 22:25:47 2018

@author: jan
"""
from flask import Flask, render_template, request, flash
from wtforms import Form, StringField
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///logins.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

class Userform(Form):
    login = StringField('login')
    password = StringField('password')


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hejhou'


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        userform = Userform(request.form)
        session = Session()
        current_user = session.query(User).filter_by(login=userform.login.data).first()
        if current_user is None:
            flash('Unknown user')
            """
            session.add(User(
                login = userform.login.data, 
                password = userform.password.data))
            """
        else:
            if current_user.password == userform.password.data:
                print('correct password')
            else:
                flash('Wrong password')
        #session.commit()
        #print('user {0} added'.format(userform.login.data))
    else:
        userform = Userform()
    return render_template('main.html', userform=userform)

if __name__ == '__main__':
    app.run(debug=True)

