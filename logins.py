#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 22:25:47 2018

@author: jan
"""
from flask import Flask, render_template, request, flash, session, redirect, url_for
from wtforms import Form, StringField, PasswordField
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///logins.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    
class Strategy(Base):
    __tablename__ = 'strategies'
    
    id = Column(Integer, primary_key=True)
    strategy = Column(String)
    loginid = Column(Integer, ForeignKey('users.id'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

class Userform(Form):
    login = StringField('login')
    password = StringField('password')

class Signupform(Userform):
    pwdcheck = PasswordField('pwdcheck')


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hejhou'


@app.route('/loggedin', methods=['GET', 'POST'])
def loggedin():
    session_db = Session()
    user = session_db.query(User).filter_by(login=session.get('current_user')).first()
    if request.method == 'POST':
        new_strategy = Strategy(
            strategy=request.form.get('newstr'),
            loginid=user.id)
        session_db.add(new_strategy)
        session_db.commit()
    strategies = session_db.query(Strategy).filter_by(loginid=user.id).all()
    session_db.close()
    return render_template('strategies.html', strategies=[s.strategy for s in strategies])

@app.route('/sigin', methods=['GET', 'POST'])
def signin():
    signupform = Signupform(request.form)
    db_session = Session()
    if request.method == 'POST':
        current_user = db_session.query(User).filter_by(login=signupform.login.data).first()
        if current_user is not None:
            flash('User already exists')
        else:
            if signupform.password.data != signupform.pwdcheck.data:
                flash("Password wasn't confirmed")
            else:
                db_session.add(User(
                login = signupform.login.data, 
                password = signupform.password.data))
                db_session.commit()
                session['current_user'] = signupform.login.data
                return redirect(url_for('loggedin'))
    else:
        pass
    db_session.close()
    return render_template('signup.html', signupform=signupform)

@app.route('/', methods=['GET', 'POST'])
def main():
    db_session = Session()
    if request.method == 'POST':
        userform = Userform(request.form)
        current_user = db_session.query(User).filter_by(login=userform.login.data).first()
        if current_user is None:
            flash('Unknown user', category='UU')
        else:
            if current_user.password == userform.password.data:
                print('correct password')
                session['current_user'] = userform.login.data
                return redirect(url_for('loggedin'))
            else:
                flash('Wrong password', category='WP')
    else:
        userform = Userform()
    db_session.close()
    return render_template('main.html', userform=userform)

if __name__ == '__main__':
    app.run(debug=True)

