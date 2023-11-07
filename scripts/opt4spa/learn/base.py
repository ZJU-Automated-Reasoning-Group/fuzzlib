# coding: utf-8
# import math
import numpy as np
from sklearn.base import BaseEstimator
# split data into train and test, deafult train_size = 0.25 and test_size = 0.75 potential to optimize
from sklearn.model_selection import train_test_split
from sklearn.metrics import *

try:
    from sklearn.externals import joblib
except Exception as ex:
    import joblib
import time
from sklearn import preprocessing
import os


class BaseModel:
    # def __init__(self, datapath="/home/linjie/dfj/mltrain/app4_exp_updated.csv", model_output="./Models",
    #             picture_path="./Pictures", log_path="./Logs/res.log", timeout=0.005, scale=False, train_idx=None):
    def __init__(self, datapath, model_output, picture_path, log_path, timeout=0.005, scale=False, train_idx=None):
        # setup datapath model output and timeout
        self.datapath = datapath
        self.picture_path = picture_path
        self.model_output = model_output
        self.timeout = timeout
        self.log_path = log_path
        self.estimator = BaseEstimator()
        self.selection_dataset = {}
        self.sere_dataset = {}
        self.threshold_dataset = {}
        self.model_dataset = {}
        self.train_idx = train_idx
        self.load_data(scale)

    def Timeout(self, data, threshold):
        return_value = []
        num_0 = 0
        num_1 = 0
        for x in data:
            if x <= threshold:
                return_value.append(1)
                num_1 += 1
            else:
                return_value.append(0)
                num_0 += 1
        return num_0, num_1, return_value

    def train(self):
        pass

    def predict(self, X_test, Y_test, method, model, load=False):

        if load:
            print("loading model")
            filename = self.datapath.split('/')[-1]
            self.estimator = joblib.load(
                self.model_output + "/" + filename + "_" + self.__class__.__name__ + "_" + self.timestr)

        Y_pred = self.estimator.predict(X_test)
        print("classification_report(Y_test, Y_pred)")
        print(classification_report(Y_test, Y_pred))

        precision, recall, f1, support = precision_recall_fscore_support(Y_test, Y_pred)

        f = open(self.log_path, 'a')

        f.write("\n====================================\n\n" +
                "Current model: " + str(model) + '\n' +
                "Current method: " + str(method) + '\n' +
                "Precision: " + str(precision) + '\n' +
                "Recall: " + str(recall) + '\n' +
                "F1: " + str(f1) + '\n' +
                "Support: " + str(support) + '\n' +
                "\n====================================\n"
                )
        f.write(classification_report(Y_test, Y_pred))
        f.write("\n")
        f.close()

        return Y_pred

    def save(self):
        # store model
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = self.datapath.split('/')[-1]
        joblib.dump(self.estimator,
                    self.model_output + "/" + filename + "_" + self.__class__.__name__ + "_" + self.timestr)

    def save_best_estimator(self):
        # store best param model
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = self.datapath.split('/')[-1]
        joblib.dump(self.best_estimator_,
                    self.model_output + "/" + filename + "_" + self.__class__.__name__ + "_" + self.timestr)

    def test(self):
        pass

    def evaluation(self):
        pass

    def ypred_random_minimum(self, Y_pred, idx_test):
        Y_pred.astype('int')
        return self.Y_raw[idx_test, Y_pred], \
               self.random_timespan[idx_test], \
               self.min_timespan[idx_test]

    def load_data(self, scale=False):
        all_data = np.loadtxt(self.datapath, skiprows=1, delimiter=',')
        row, col = all_data.shape
        # train is selected, becuase 5 solvers hence -10
        print("Selecting column - ", os.environ["train_x_idx"], "for training set")
        self.train_X = all_data[:, : col - int(os.environ["train_x_idx"])]

        if scale:
            self.scale = preprocessing.MinMaxScaler().fit(self.train_X)
            self.train_X = self.scale.transform(self.train_X)

        self.indices = np.arange(row)

        '''only used for test distribution'''
        self.train_ys = []
        start_idx = -1
        for y_idx in range(int(os.environ["train_y_idx"])):
            self.train_ys.append(all_data[:, start_idx])
            start_idx -= 2

        Y_raw = np.vstack(self.train_ys)
        print("-" * 50)
        print(Y_raw.shape)
        print("-" * 50)
        # All y with time span
        self.Y_raw = Y_raw.T

        # index of solver who has minimum timespan
        min_col = self.Y_raw.argmin(1)
        self.min_col = min_col.T

        # minimum timespan of all solvers
        min_timespan = self.Y_raw.min(1)
        self.min_timespan = min_timespan.T

        # generate random timespan from all solvers
        # first, generate a row size array with each element is random from 0 - 4
        self.random_select_id = np.random.randint(min(3, int(os.environ["train_y_idx"])), size=row)
        # choose
        self.random_timespan = np.choose(self.random_select_id, Y_raw)

        self.train_ys = []
        start_idx = -1
        for y_idx in range(int(os.environ["train_y_idx"])):
            _, _, y = self.Timeout(all_data[:, start_idx], self.timeout)
            self.train_ys.append(y)
            start_idx -= 2
        Y = np.vstack(self.train_ys + [min_col.T])
        self.train_Y = Y.T

    def SplitData(self):
        X_train, X_test, Y_train, Y_test = train_test_split(self.train_X, self.train_Y, test_size=0.2, random_state=42)

    def select_param(self):
        pass

    def feature_selection(self):
        pass
