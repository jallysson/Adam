import os
import sys
sys.path.append('..')
import json
import pickle
import pandas as pd
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from settings import TOKEN
from datetime import datetime
from algorithms.classification.svm import training

def _load_model(request, version=''):
    return pickle.load(open(
        'models/{}/{}/{};{}.sav'.format(
            request.json.get('typeLearning').lower(),
            request.json.get('model').lower(),
            request.json.get('modelName').lower(),
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
    version = datetime.now().isoformat()
    dataset = pd.read_csv(
        'datasets/training/{}.csv'.format(request.json.get('datasetName'))
    ) 
    targets = dataset[request.json.get('targetColumn')].values
    features = dataset.drop(columns=[request.json.get('targetColumn')]).values
    model = training(features, targets)

    file = 'models/{}/{}/{};{}.sav'.format(
        request.json.get('typeLearning').lower(),
        request.json.get('model').lower(),
        request.json.get('modelName').lower(),
        version
    )

    pickle.dump(model, open(file, 'wb'))

    dropbox_path = '/training/{}_{}'.format(
        file.split(';')[0].replace('/', '_'),
        file.split('/')[-1]
    )

    request.json['features'] = list(dataset.columns.values)

    if upload_model_file_to_dropbox(file, dropbox_path):
        response = model_parameters(request, version)
        os.remove(file)       
        return response

    return 'Model training failure'

def upload_model_file_to_dropbox(file, dropbox_path):
    dbx = dropbox.Dropbox(TOKEN)
    with open(file, 'rb') as f:
        try:
            dbx.files_upload(f.read(), dropbox_path, mode=WriteMode('overwrite'))
            return True
        except ApiError as err:
            print(err)

def model_prediction(request):
    model = _load_model(request)
    dataset = pd.read_csv(
        'datasets/prediction/{}.csv'.format(request.json.get('datasetName'))
    )
    predictions = model.predict(dataset.values)
    request.json['predictions'] = list(predictions)

    return request.json

def models():
    dbx = dropbox.Dropbox(TOKEN)
    files = [entry.name for entry in dbx.files_list_folder('/production').entries]
    
    models = []
    for file in files:
        file = file.split('_')
        file = {
            "typeLearning": file[1],
            "model": file[2],
            "modelName": file[-1].replace('.sav', '').split(';')[0].upper(),
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