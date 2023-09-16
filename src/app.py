import sys
sys.path.append('srv/freshnessmodel/Freshness-Model-VTHacks/src/models')
import utils

from flask import Flask, jsonify

app = Flask(__name__)

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

@app.route('/train_and_evaluate', methods=['GET'])
def train_and_evaluate():
    model = utils.train_and_evaluate_cnn()
    # You can return any relevant information about the model here, for example:
    return jsonify({"message": "Model trained and evaluated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
