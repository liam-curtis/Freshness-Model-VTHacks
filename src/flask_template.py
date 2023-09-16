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
 
# Configure the database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://davidjdeg2@Snowden37606!@70.161.68.15/Website_DB'

# Create a SQLAlchemy instance
db = SQLAlchemy(app)

cursor = db.session.connection().cursor()

# Execute a simple SQL query
cursor.execute("SELECT * FROM User")
# Fetch the results
results = cursor.fetchall()
user_data = [{'id': result[0], 'username': result[1], 'email': result[2]} for result in results]
print(user_data)

#Close the curso
cursor.close()

@app.route('/')
def index():
    return render_template('index.html')
 
if __name__=='__main__':
    app.run(debug = True)