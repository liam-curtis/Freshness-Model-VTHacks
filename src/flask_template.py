import os
from flask import Flask, render_template, request, url_for, redirect, flash
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

# @app.route('/')
# def welcome():
#     return "This is the home page of Flask Application"
 
# Configure the database connection URI
#db_password = os.environ.get('DATABASE_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://davidjdeg2:Snowden37606!@70.161.68.15/Website_DB'

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

# @app.route('/register', methods=['GET', 'POST'])
# def registerUser():
#     if request.method == 'POST':
#         username = request.form['user']
#         password = request.form['user_pass']
#         email = request.form['mail']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']

#     return render_template('login.html')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

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
        #unique_result[0]=1
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
        return render_template('success.html')
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
        #unique_result[0]=1
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