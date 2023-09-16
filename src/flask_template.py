import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text
 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

# @app.route('/')
# def welcome():
#     return "This is the home page of Flask Application"
 
# Configure the database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://davidjdeg2:Snowden37606!@70.161.68.15/Website_DB'

# # Create a SQLAlchemy instance
db = SQLAlchemy(app)
app.app_context().push()
#print(type(db))
cursor = db.session.connection()

# # Execute a simple SQL query
try:  
    query = text("SELECT * FROM User;")
    result = db.session.execute(query)
except Exception as e:
    print(e)
# # Fetch the results
row = result.fetchall()
user_data = [{'id': result[0], 'username': result[1], 'email': result[2]} for result in row]
print(user_data)

# #Close the curso
cursor.close()

@app.route('/')
def index():
    return render_template('index.html')
 
if __name__=='__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)