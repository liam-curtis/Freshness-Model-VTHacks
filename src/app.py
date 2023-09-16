import sys
sys.path.append('srv/freshnessmodel/Freshness-Model-VTHacks/src')
from utils import train_and_evaluate, load_images_as_tensors

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

@app.route('/train_and_evaluate', methods=['GET'])
def train_and_evaluate():
    model = utils.train_and_evaluate_cnn()
    # You can return any relevant information about the model here, for example:
    return jsonify({"message": "Model trained and evaluated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
