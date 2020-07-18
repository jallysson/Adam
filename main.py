from settings import HOST, PORT
from flask import Flask, jsonify, request
from management.manage import model_parameters, model_predict
import sys

app = Flask(__name__)

@app.route('/')
def up():
	return 'DARK UP'

@app.route('/model_parameters', methods=['GET'])
def _get_model_parameters():
    response = model_parameters(request)
    return jsonify(response)

@app.route('/model_predict', methods=['GET'])
def _get_model_predict():
    response = model_predict(request)
    return jsonify(response)

app.run(host=HOST, port=PORT, debug=True)