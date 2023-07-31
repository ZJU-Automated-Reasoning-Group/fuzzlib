# coding: utf-8
from sklearn.svm import SVR
from mlp import *
from svc import *
from knn import *
from random_forest import *
from lgb import *
from base import *

from feature_selection import *
from sklearn.model_selection import train_test_split
import os
import matplotlib.pyplot as plt
import time

# Here key data structure
m_global_datapath = "/home/linjie/dfj/mltrain/app4_exp_updated.csv"
m_global_model_output = "Lab/muli/Models"
m_global_picutre_path = "Lab/muli/Pictures"
m_global_log_path = "Lab/muli/Logs/res.log"


# print("this is shape of model")

def splitData(X, Y, indices=None):
    if indices is None:
        return train_test_split(X, Y, test_size=0.2, random_state=42)

    X_train, X_test, Y_train, Y_test, idx_train, idx_test = train_test_split(X, Y, indices, test_size=0.2,
                                                                             random_state=42)
    return X_train, X_test, Y_train, Y_test, idx_test

def run_muli(args):
    # model = BaseModel(datapath="/home/linjie/dfj/mltrain/app4_exp_updated.csv",
    # model_output="Lab/muli/Models",
    # picture_path = "Lab/muli/Pictures",
    # log_path="Lab/muli/Logs/res.log")
    model = BaseModel(datapath=m_global_datapath, model_output=m_global_model_output,
                      picture_path=m_global_picutre_path, log_path=m_global_log_path)

    # print("this is shape of model")
    # print(model.train_X.shape, model.train_Y.shape)
    svc = skl_svm()
    mlp = skl_mlp()
    knn = KNeightbor()
    rnf = random_forest()
    lgb = Lgb_Model()

    mlp_selection_dataset, mlp_sere_dataset, mlp_threshold_dataset, mlp_model_dataset = \
        feature_selection(model.train_X, model.train_Y[:, int(os.environ["train_y_idx"])])
    print("reach feature_frequency")
    feature_frequency = [0] * model.train_X.shape[1]


    for key, value in mlp_selection_dataset.items():
        f = open(model.log_path, 'a')
        f.write(key)
        f.write("\n")
        f.close()
        print("reach for key, value in mlp_selection, f.close()")
        # key = 'fpr'
        # value = mlp_selection_dataset[key]
        # get data from feature selection result
        print("Current feature selection method is : " + key)
        data = value['data']

        # draw pictures
        fig, ax = plt.subplots(1, 3, figsize=(6, 2), dpi=400)
        fig.canvas.set_window_title('Evaluation')

        features = value['feature']
        feature_used = []

        for index, feature in enumerate(features):
            if feature:
                feature_used.append(index)

        X_train, X_test, Y_train, Y_test, idx_test = splitData(data, model.train_Y[:, int(os.environ["train_y_idx"])],
                                                               indices=model.indices)
        params_kn = {
            'n_neighbors': [5, 10, 15, 20, 25],
            'weights': ['uniform', 'distance']
            # 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
        }
        # kn2 = KNeighborsClassifier()
        # grid_knn = GridSearchCV(estimator=kn2,
        #                        param_grid=params_kn,
        #                        scoring='accuracy',
        #                        cv=5,
        #                        verbose=1,
        #                        n_jobs=-1)
        print("knn PROCESS")
        # grid_knn.fit(X_train, Y_train)
        if args.train_mode == "grid_search":
            print("grid search training")
            knn.grid_train(X_train, Y_train, params_kn)
        else:
            knn.train(X_train, Y_train)
        # # print(knn.__class__.__name__)
        y_prd = knn.predict(X_test, Y_test, key, knn.__class__.__name__, load=True)
        #
        y_pred, y_random, y_best = knn.ypred_random_minimum(y_prd, idx_test)
        f = open(model.log_path, 'a')
        f.write("\n====================================\n\n" +
                "Y_pred_sum: " + str(np.sum(y_prd)) +
                "y_random_sum: " + str(np.sum(y_random)) +
                "y_best_sum: " + str(np.sum) +
                "\n====================================\n"
                )

        f.close()

        # draw picture for knn
        ax[0].scatter(np.log(y_best), np.log(y_random), c="red", s=0.0008, label="red: best/random")
        ax[0].scatter(np.log(y_best), np.log(y_pred), c="green", s=0.0008, label="green: best/pred")

        ax[0].legend(loc=4, fontsize='xx-small', scatterpoints=1)
        ax[0].set_title("KNN", fontsize='x-small')
        ax[0].grid(True)
        # ax[1].grid(True)

        print("MLP PROCESS")
        # mlp2 = MLPClassifier(max_iter=100)
        params_mlp = {
            'hidden_layer_sizes': [(50, 50, 50), (50, 100, 50), (100,)],
            'activation': ['tanh', 'relu'],
            'solver': ['sgd', 'adam'],
            'alpha': [0.0001, 0.05],
            'learning_rate': ['constant', 'adaptive'],
        }
        # grid_mlp = GridSearchCV(mlp2, params_mlp, n_jobs=-1, cv=3)
        # grid_mlp.fit(X_train, Y_train)
        if args.train_mode == "grid_search":
            print("grid search training")
            mlp.select_param(X_train, Y_train)
        else:
            mlp.train(X_train, Y_train)
        y_prd = mlp.predict(X_test, Y_test, key, mlp.__class__.__name__, load=True)

        y_pred, y_random, y_best = mlp.ypred_random_minimum(y_prd, idx_test)
        f = open(model.log_path, 'a')
        f.write("\n====================================\n\n" +
                "Y_pred_sum: " + str(np.sum(y_prd)) +
                "y_random_sum: " + str(np.sum(y_random)) +
                "y_best_sum: " + str(np.sum) +
                "\n====================================\n"
                )

        f.close()

        # draw picture for MLP
        ax[1].scatter(np.log(y_best), np.log(y_random), c="red", s=0.0008, label="red: best/random")
        ax[1].scatter(np.log(y_best), np.log(y_pred), c="green", s=0.0008, label="green: best/pred")

        ax[1].legend(loc=4, fontsize='xx-small')
        ax[1].set_title("MLP", fontsize='x-small')
        ax[1].grid(True)
        # ax[1].grid(True)

        print("rnf PROCESS")
        # params_rnf = {'bootstrap': [True, False],
        #      'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
        #      'max_features': ['auto', 'sqrt'],
        #      'min_samples_leaf': [1, 2, 4],
        #      'min_samples_split': [2, 5, 10],
        #      'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}
        # rnf2 =  RandomForestRegressor(random_state = 42)
        # grid_rnf = GridSearchCV(estimator=rnf2, param_grid=params_rnf, cv=5)
        if args.train_mode == "grid_search":
            print("grid search training")
            rnf.select_param(X_train, Y_train)
        else:
            rnf.train(X_train, Y_train)
        y_prd = rnf.predict(X_test, Y_test, key, rnf.__class__.__name__, load=True)

        y_pred, y_random, y_best = rnf.ypred_random_minimum(y_prd, idx_test)
        f = open(model.log_path, 'a')
        f.write("\n====================================\n\n" +
                "Y_pred_sum: " + str(np.sum(y_prd)) +
                "y_random_sum: " + str(np.sum(y_random)) +
                "y_best_sum: " + str(np.sum) +
                "\n====================================\n"
                )

        f.close()
        # draw picture for rnf
        ax[2].scatter(np.log(y_best), np.log(y_random), c="red", s=0.0008, label="red: best/random")
        ax[2].scatter(np.log(y_best), np.log(y_pred), c="green", s=0.0008, label="green: best/pred")

        ax[2].legend(loc=4, fontsize='xx-small')
        ax[2].set_title("RNF", fontsize='x-small')
        ax[2].grid(True)
        # ax[1].grid(True)

        indices = np.argsort(rnf.estimator.feature_importances_)[::-1]
        f = open(model.log_path, 'a')
        f.write("\n====================================\n\n" +
                "Feature Importance: \n"
                )

        for index in indices:
            f.write(str(feature_used[index]) + ' ')

        f.write("\n====================================\n")
        f.close()

        # save picture
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = model.datapath.split('/')[-1]
        plt.savefig(model.picture_path + "/" + filename + "_" + key + "_" + timestr + ".png")
        plt.close()

        # svm train
        grid_svc = GridSearchCV(
            estimator=SVR(kernel='rbf'),
            param_grid={
                'C': [0.1, 1, 100, 1000],
                'epsilon': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10],
                'gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5]
            },
            cv=5, scoring='neg_mean_squared_error', verbose=0, n_jobs=-1)
        print("svm PROCESS")
        if args.train_mode == "grid_search":
            print("grid search training")
            svc.select_param(X_train, Y_train)
        else:
            svc.train(X_train, Y_train)

        # lgb train
        params_lgb = {'learning_rate': [0.005, 0.01],
                      'n_estimators': [8, 16, 24],
                      'num_leaves': [6, 8, 12, 16],
                      # large num_leaves helps improve accuracy but might lead to over-fitting
                      'boosting_type': ['gbdt', 'dart'],  # for better accuracy -> try dart
                      'objective': ['binary'],
                      'max_bin': [255, 510],
                      # large max_bin helps improve accuracy but might slow down training progress
                      'random_state': [500],
                      'colsample_bytree': [0.64, 0.65, 0.66],
                      'subsample': [0.7, 0.75],
                      'reg_alpha': [1, 1.2],
                      'reg_lambda': [1, 1.2, 1.4]}
        # lgb2 = lgb.LGBMClassifier(num_leaves=32, learning_rate=0.02, n_estimators=600)
        # grid_lgb = GridSearchCV(lgb2, param_grid=params_lgb, scoring='recall')
        print("lgb PROCESS")
        # grid_lgb.fit(X_train,Y_train)
        if args.train_mode == "grid_search":
            print("grid search training")
            lgb.select_param(X_train, Y_train)
        else:
            lgb.train(X_train, Y_train)
        y_prd = lgb.predict(X_test, Y_test, key, lgb.__class__.__name__, load=True)
        y_pred, y_random, y_best = lgb.ypred_random_minimum(y_prd, idx_test)
        f = open(model.log_path, 'a')
        f.write("\n================lgb process====================\n\n" +
                "Y_pred_sums: " + str(np.sum(y_prd)) +
                "y_random_sums: " + str(np.sum(y_random)) +
                "y_best_sums: " + str(np.sum) +
                "\n====================================\n"
                )

        f.close()

    feature_frequency_res = [x for x in feature_frequency]

    f = open(model.log_path, 'a')
    f.write("\n====================================\n\n" +
            "Feature frequency: \n"
            )
    for item in feature_frequency_res:
        f.write(str(item) + ' ')

    f.write("\n====================================\n")
    f.close()


if __name__ == "__main__":

    import argparse
    import configparser

    parser = argparse.ArgumentParser(description='mode selection for training')
    parser.add_argument('--train_mode', dest='train_mode', help='normal training and gird training', default='off',
                        type=str)
    parser.add_argument('--config', dest='config', default='no', type=str)
    parser.add_argument('--solvermode', dest='solvermode', default='z3seq', type=str)
    args = parser.parse_args()

    if args.solvermode != "z3seq" and args.solvermode != "z3str3":
        print("Please specify the solver mode via --solvermode")
        exit(0)

    m_solver_mode = args.solvermode

    if args.config != 'no':
        m_config = configparser.ConfigParser()
        m_config.read(args.config)
        if args.solvermode == "z3seq":
            m_global_datapath = m_config['Z3SEQ']['DataPath']
            m_global_model_output = m_config['Z3SEQ']['ModelOutput']
            m_global_picutre_path = m_config['Z3SEQ']['PicturePath']
            m_global_log_path = m_config['Z3SEQ']['LogPath']
        elif args.solvermode == "z3str3":
            m_global_datapath = m_config['Z3STR3']['DataPath']
            m_global_model_output = m_config['Z3STR3']['ModelOutput']
            m_global_picutre_path = m_config['Z3STR3']['PicturePath']
            m_global_log_path = m_config['Z3STR3']['LogPath']

    run_muli(args)
    # run_bin(args)
