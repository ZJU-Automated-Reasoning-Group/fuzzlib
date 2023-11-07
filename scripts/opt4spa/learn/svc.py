# coding: utf-8
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
# import sys
# import joblib
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import classification_report
from base import BaseModel
from feature_selection import *
# from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support, accuracy_score
import numpy as np


class skl_svm(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.model_name = "svm.pkl"

    def train(self, X_train, Y_train, C=1e3, gamma=0.1, verbose=99):
        # self.estimator = SVC(C=C, gamma=gamma, verbose=verbase)
        self.estimator = LinearSVC(verbose=verbose, max_iter=10000)

        # training
        self.estimator.fit(X_train, Y_train)

        # store model
        self.save()

    # def predict(self, X_test, Y_test):
    #     Y_pred = self.estimator.predict(X_test)
    #     print(classification_report(Y_test, Y_pred))

    def select_param(self, X_train, Y_train):
        gamma_space = np.logspace(-5, -1)
        C_space = np.logspace(-5, 2)
        cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
        tune_param = {
            'C': C_space,
            'gamma': gamma_space
        }
        svm = GridSearchCV(SVC(), param_grid=tune_param, cv=cv, n_jobs=-1, scoring='accuracy', verbose=5)
        svm.fit(X_train, Y_train)
        self.best_estimator_ = svm.best_estimator_
        filepath = "/home/linjie/dfj/mltrain/train/best_param.txt"
        f = open(filepath, "a+")
        f.write(str(self.best_estimator_))
        f.close()
        # print(svm.best_estimator_)
        # save best model
        self.save_best_estimator()
        # joblib.dump(svm.best_estimator_,  self.model_output + "/" + 'svm_best.pkl', compress=1)

        means = svm.cv_results_['mean_test_score']
        for mean, param in zip(means, svm.cv_results_['params']):
            print("%0.4f for %r" % (mean, param))
