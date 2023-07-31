# import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
# from sklearn.datasets import make_classification

from base import BaseModel
from feature_selection import *


class random_forest(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.model_name = self.__class__.__name__

    def train(self, X_test, Y_test, n_estimator=100):
        self.estimator = RandomForestClassifier(n_estimators=n_estimator)
        self.estimator.fit(X_test, Y_test)

        # store model
        self.save()

    def select_param(self, X_test, Y_test):
        params_rnf = {'max_features': ['auto', 'sqrt'],
                      'min_samples_leaf': [1, 2, 4],
                      'min_samples_split': [2, 5, 10],
                      'n_estimators': [100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}

        grid_rnf = GridSearchCV(estimator=RandomForestClassifier(), param_grid=params_rnf, cv=5, scoring='accuracy',
                                verbose=5, n_jobs=-1)
        grid_rnf.fit(X_test, Y_test)
        self.best_estimator_ = grid_rnf.best_estimator_
        # print(grid_rnf.best_estimator_)
        filepath = "/home/linjie/dfj/mltrain/train/best_param.txt"
        f = open(filepath, "a+")
        f.write(str(self.best_estimator_))
        f.close()

        # store  best model
        self.save_best_estimator()

    def feature_selection(self):
        self.selection_dataset, self.sere_dataset, self.threshold_dataset, self.model_dataset = feature_selection(
            self.X_train, self.Y_train)


if __name__ == '__main__':
    clf = RandomForestClassifier(n_estimators=100, max_depth=2,
                                 random_state=0)
