import sys
from settings import HOST, PORT
from flask import Flask, jsonify, request
from flask_cors import CORS

from management.manage import (
    model_parameters,
    model_prediction,
<<<<<<< Updated upstream
    model_training
=======
    model_training,
    models,
    delete_model
>>>>>>> Stashed changes
)

app = Flask(__name__)
CORS(app)

@app.route('/')
def up():
	return 'Adam up'

@app.route('/model_training', methods=['POST'])
def _post_model_training():
    response = model_training(request)
    return jsonify(response)

@app.route('/model_parameters', methods=['GET'])
def _get_model_parameters():
    response = model_parameters(request)
    return jsonify(response)

@app.route('/model_prediction', methods=['POST'])
def _post_model_prediction():
    response = model_prediction(request)
    return jsonify(response)

<<<<<<< Updated upstream
=======
@app.route('/models', methods=['GET'])
def _get_models():
    response = models()
    return jsonify(response)

@app.route('/delete_model', methods=['POST'])
def _post_model():
    response = delete_model(request)
    return jsonify(response)

>>>>>>> Stashed changes
app.run(host=HOST, port=PORT, debug=True)