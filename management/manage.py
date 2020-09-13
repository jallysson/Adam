import os
import sys
sys.path.append('..')
import json
import pickle
import pandas as pd
from datetime import datetime
from algorithms.classification.svm import training

def _load_model(request, version=''):
    return pickle.load(open(
        'models/{}/{}/{};{}.sav'.format(
            request.json.get('typeLearning'),
            request.json.get('model'),
            request.json.get('modelName'),
            version
        ),'rb')
    )

def model_parameters(request, version=''):
    model = _load_model(request, version)
    request.json['parameters'] = json.loads('{' + str(model) \
        .replace('SVC(', '"') \
        .replace(')', '"') \
        .replace('=', '":"') \
        .replace(',', '", "') \
        .replace(' ', '') \
        .replace("'", '') \
        .replace('\n', '') + '}'
    )
    return request.json

def model_training(request):
    version = datetime.now()
    dataset = pd.read_csv(
        'datasets/training/{}.csv'.format(request.json.get('datasetName'))
    ) 
    targets = dataset[request.json.get('targetColumn')].values
    features = dataset.drop(columns=[request.json.get('targetColumn')]).values
    model = training(features, targets)
    pickle.dump(model, open(
        'models/{}/{}/{};{}.sav'.format(
            request.json.get('typeLearning'),
            request.json.get('model'),
            request.json.get('modelName'),
            version
        ), 'wb')
    )
    request.json['features'] = list(dataset.columns.values)
    return model_parameters(request, version)

def model_prediction(request):
    model = _load_model(request)
    dataset = pd.read_csv(
        'datasets/prediction/{}.csv'.format(request.json.get('datasetName'))
    )
    predictions = model.predict(dataset.values)
    request.json['predictions'] = list(predictions)

    return request.json

def models():
    files = list()
    for (dirpath, dirnames, filenames) in os.walk('models'):
        files += [os.path.join(dirpath, file) for file in filenames if '.sav' in file] 
    models = []
    for file in files:
        file.replace('/', '\\')
        file = file.split('\\')
        file = {
            "typeLearning": file[-3],
            "model": file[-2],
            "modelName": file[-1].replace('.sav', '').split(';')[0],
            "version": file[-1].replace('.sav', '').split(';')[1]
        }
        models.append(file)
    return models

def delete_model(request):
    os.remove('models/{}/{}/{};{}.sav'.format(
            request.json.get('typeLearning'),
            request.json.get('model'),
            request.json.get('modelName'),
            request.json.get('version')
    ))
    return 'File removed'