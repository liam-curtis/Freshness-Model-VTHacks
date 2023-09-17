import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from PIL import Image
from utils import load_image_as_tensor, predict_image
import torch
import torch.nn as nn
import sys
import importlib.util

# Specify the path to the module
module_path = "./models/cnn.py"

# Create a module spec from the file location
module_spec = importlib.util.spec_from_file_location("cnn", module_path)

# Create and load the module
cnn = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(cnn)

# Access the CNNModel class from the loaded module
from cnn import CNNModel
 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'images'
 
# Configure the database connection URI
#db_password = os.environ.get('DATABASE_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://davidjdeg2:Snowden37606!@70.161.68.15/Website_DB'

# Create a SQLAlchemy instance
db = SQLAlchemy(app)
app.app_context().push()
cursor = db.session.connection()

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

model = CNNModel()

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['user_pass']

        unique_query = text('CALL VerifyUsernamePassword(:username, :password, @result);')
        db.session.execute(unique_query, {'username': username, 'password': password})
        result = db.session.execute(text('SELECT @result')).scalar()
        print(result)

        # Access the value of the output parameter directly
        if result == 1:
            # Call the stored procedure to insert the user data into the database
            return redirect(url_for('upload'))  # Redirect to the login page after registration
        else:
            flash('Username or password is incorrect', 'danger')

    return render_template('login.html')

@app.route('/upload', methods=['GET',"POST"])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        uploaded_filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_filename)
        pil_image = load_image_as_tensor(Image.open(image_path))
        model.load_state_dict(torch.load('model.pth'))
        message = predict_image(model, pil_image)
        return render_template('success.html', message=message, image_path=image_path)
    return render_template('upload.html', form=form)

@app.route('/about_us')
def about_us():
    return render_template('about.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['user_pass']
        email = request.form['mail']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        unique_query = text('CALL VerifyUniqueNameEmail(:username, :email, @result);')
        db.session.execute(unique_query, {'username': username, 'email': email})
        result = db.session.execute(text('SELECT @result')).scalar()
        print(result)

        # Access the value of the output parameter directly
        if result == 1:
            # Call the stored procedure to insert the user data into the database
            insert_query = text('CALL InsertUserWithHashedPassword(:username, :password, :email, :first_name, :last_name);')
            insert_values = {
                'username': username,
                'password': password,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
            db.session.execute(insert_query, insert_values)
            db.session.commit()  # Commit the transaction
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))  # Redirect to the login page after registration
        else:
            flash('Username or email is already in use. Please choose another.', 'danger')

    return render_template('register.html')

cursor.close()

@app.route('/')
def index():
    return render_template('index.html')
 
if __name__=='__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)