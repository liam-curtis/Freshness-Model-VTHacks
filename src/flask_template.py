import os
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text
 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'testing'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return render_template('success.html')
    return render_template('index.html', form=form)
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/about_us')
def about_us():
    return render_template('about.html')
@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/register')
def register():
    return  render_template('register.html')

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