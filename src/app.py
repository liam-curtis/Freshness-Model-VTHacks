import sys
sys.path.append('srv/freshnessmodel/Freshness-Model-VTHacks/src/models')
import utils

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/train_and_evaluate', methods=['GET'])
def train_and_evaluate():
    model = utils.train_and_evaluate_cnn()
    # You can return any relevant information about the model here, for example:
    return jsonify({"message": "Model trained and evaluated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
