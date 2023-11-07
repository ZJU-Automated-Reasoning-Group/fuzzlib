# coding: utf-8
# import numpy as np
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import lightgbm as lgb
from base import BaseModel
from feature_selection import *


class Lgb_Model(BaseModel):
    def __init__(self):
        BaseModel.__init__(self, model_output="Lab/muli/Models")
        self.model_name = self.__class__.__name__

    def train(self, X_test, Y_test, multi_class=False, vx=0, vy=0):
        if multi_class:
            objective = 'multiclass'
        else:
            objective = 'binary'
        watchlist = [(X_test, Y_test), (vx, vy)]
        self.estimator = lgb.LGBMClassifier(num_leaves=32, learning_rate=0.02, n_estimators=600)
        self.estimator.fit(X_test, Y_test)

        # store model
        self.save()

    def select_param(self, X_test, Y_test, multi_class=False, vx=0, vy=0):
        if multi_class:
            objective = 'multiclass'
        else:
            objective = 'binary'
        watchlist = [(X_test, Y_test), (vx, vy)]
        params_lgb = {'learning_rate': [0.005, 0.01],
                      'n_estimators': [8, 16, 24],
                      'num_leaves': [6, 8, 12, 16],
                      # large num_leaves helps improve accuracy but might lead to over-fitting
                      'boosting_type': ['gbdt', 'dart'],  # for better accuracy -> try dart
                      'objective': [objective],
                      'max_bin': [255, 510],
                      # large max_bin helps improve accuracy but might slow down training progress
                      'random_state': [500],
                      'colsample_bytree': [0.64, 0.65, 0.66],
                      'subsample': [0.7, 0.75],
                      'reg_alpha': [1, 1.2],
                      'reg_lambda': [1, 1.2, 1.4]}
        self.estimator = lgb.LGBMClassifier(num_leaves=32, learning_rate=0.02, n_estimators=600)
        grid_lgb = GridSearchCV(estimator=self.estimator, param_grid=params_lgb, scoring='roc_auc', verbose=5,
                                n_jobs=-1)
        grid_lgb.fit(X_test, Y_test)
        self.best_estimator_ = grid_lgb.best_estimator_
        filepath = "/home/linjie/dfj/mltrain/train/best_param.txt"
        f = open(filepath, "a+")
        f.write(str(self.best_estimator_))
        f.close()
        # print(grid_lgb.best_estimator_)

        # save best model
        self.save_best_estimator()

    def feature_selection(self):
        self.selection_dataset, self.sere_dataset, self.threshold_dataset, self.model_dataset = feature_selection(
            self.X_train, self.Y_train)


if __name__ == '__main__':
    pass
    # clf = RandomForestClassifier(n_estimators=100, max_depth=2,
    #                         random_state=0)
