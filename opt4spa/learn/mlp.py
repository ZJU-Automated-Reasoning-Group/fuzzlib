# coding: utf-8

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support, accuracy_score
# import numpy as np
# from sklearn import preprocessing
# import sys
# import joblib
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
# import time
from base import BaseModel
# from feature_selection import *


class skl_mlp(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.model_name = "mlp.pkl"

    def train(self, train_X, train_Y):
        self.estimator = MLPClassifier(hidden_layer_sizes=(51,), activation='logistic', solver='sgd', verbose=5,
                                       max_iter=10000, random_state=22)
        self.estimator.fit(train_X, train_Y)

        # store model
        self.save()

        # def predict(self, X_test, Y_test):

    #     Y_pred = self.estimator.predict(X_test)
    #     print(classification_report(Y_test, Y_pred))

    def select_param(self, X, Y):
        H_space = [x for x in range(20, 200, 2)]
        cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
        tune_param = {
            'hidden_layer_sizes': H_space,
            'activation': ['logistic', 'identity', 'tanh', 'relu'],
            'tol': [1e-4],
            'max_iter': [100]
        }
        MLP = GridSearchCV(
            MLPClassifier(),
            tune_param,
            cv=cv,
            scoring='accuracy',
            verbose=5,
            n_jobs=-1
        )
        MLP.fit(X, Y)
        self.best_estimator_ = MLP.best_estimator_
        filepath = "/home/linjie/dfj/mltrain/train/best_param.txt"
        f = open(filepath, "a+")
        f.write(str(self.best_estimator_))
        f.close()
        self.save_best_estimator()
        means = MLP.cv_results_['mean_test_score']
        # joblib.dump(MLP.best_estimator_, self.model_output + "/" + 'mlp_best.pkl', compress=1)
        self.best_activation = MLP.best_params_['activation']
        self.best_H = int(MLP.best_params_['hidden_layer_sizes'])

        for mean, param in zip(means, MLP.cv_results_['params']):
            print("%0.4f for %r" % (mean, param))
