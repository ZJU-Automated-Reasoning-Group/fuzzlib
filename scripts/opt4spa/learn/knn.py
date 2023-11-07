# coding: utf-8
# import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from base import BaseModel
# import joblib
from feature_selection import *


class KNeightbor(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.model_name = self.__class__.__name__

    def train(self, X_test, Y_test, n_neighbor=5):
        self.estimator = KNeighborsClassifier(n_neighbors=n_neighbor)
        self.estimator.fit(X_test, Y_test)

        # store model
        self.save()

    def grid_train(self, X_test, Y_test, params_kn):
        self.estimator = KNeighborsClassifier()
        grid_knn = GridSearchCV(estimator=KNeighborsClassifier(), param_grid=params_kn, scoring='accuracy', cv=5,
                                verbose=1, n_jobs=-1)
        grid_knn.fit(X_test, Y_test)
        self.best_estimator_ = grid_knn.best_estimator_
        filepath = "/home/linjie/dfj/mltrain/train/best_param.txt"
        f = open(filepath, "w+")
        f.write(str(self.best_estimator_))
        f.close()
        # print(self.estimator,grid_knn.best_estimator_)
        self.save_best_estimator()

    def feature_selection(self):
        self.selection_dataset, self.sere_dataset, self.threshold_dataset, self.model_dataset = feature_selection(
            self.X_train, self.Y_train)


if __name__ == '__main__':
    pass
