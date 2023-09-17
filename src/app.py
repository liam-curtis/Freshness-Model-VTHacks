import sys
sys.path.append('srv/freshnessmodel/Freshness-Model-VTHacks/src')
from utils import train_and_evaluate


model = utils.train_and_evaluate_cnn()
# You can return any relevant information about the model here, for example:
return jsonify({"message": "Model trained and evaluated successfully!"})

