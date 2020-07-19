import sys
from settings import HOST, PORT
from flask import Flask, jsonify, request
from management.manage import (
    model_parameters,
    model_prediction,
    model_training
)

app = Flask(__name__)

@app.route('/')
def up():
	return 'DARK UP'

@app.route('/model_training', methods=['POST'])
def _get_model_training():
    response = model_training(request)
    return jsonify(response)

@app.route('/model_parameters', methods=['GET'])
def _get_model_parameters():
    response = model_parameters(request)
    return jsonify(response)

@app.route('/model_prediction', methods=['POST'])
def _get_model_prediction():
    response = model_prediction(request)
    return jsonify(response)

app.run(host=HOST, port=PORT, debug=True)