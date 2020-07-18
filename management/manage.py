import pickle
import sys
sys.path.append('..')
import json

def _load_model(request):
    return pickle.load(open(
        'models/' + \
        request.json.get('typeLearning') + '/' + \
        request.json.get('model') + '/' +\
        request.json.get('modelName') + \
        '.sav', 'rb'
    ))

def model_parameters(request):
    model = _load_model(request)

    return json.loads('{' + str(model) \
        .replace('SVC(', '"') \
        .replace(')', '"') \
        .replace('=', '":"') \
        .replace(',', '", "') \
        .replace(' ', '') \
        .replace("'", '') \
        .replace('\n', '') + '}'
    )

def model_predict(request):
    model = _load_model(request)
    return str(
        model.predict([[2., 2.]])
    )