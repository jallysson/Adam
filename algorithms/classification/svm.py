from sklearn import svm
import pickle

clf = svm.SVC()

def training(features, targets, parameters=None):
    if parameters is not None:
        pass
    else:
        return clf.fit(features, targets)