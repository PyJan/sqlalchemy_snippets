#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 22:25:47 2018

@author: jan
"""
from flask import Flask, render_template, request
from wtforms import Form, StringField

app = Flask(__name__)


class Userform(Form):
    login = StringField('login')
    password = StringField('password')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        userform = Userform(request.form)
        print(userform.login.data, userform.password.data)
    else:
        userform = Userform()
    return render_template('main.html', userform=userform)

if __name__ == '__main__':
    app.run(debug=True)

