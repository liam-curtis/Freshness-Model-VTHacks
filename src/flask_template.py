import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
 
# @app.route('/')
# def welcome():
#     return "This is the home page of Flask Application"
 
@app.route('/')
def index():
    return render_template('index.html')
 
if __name__=='__main__':
    app.run(debug = True)