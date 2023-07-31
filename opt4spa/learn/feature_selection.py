import numpy as np
from sklearn.datasets import load_iris
from sklearn.feature_selection import *
# from sklearn.svm import LinearSVC

selections = [
    'percentile',
    'k_best',
    'fpr',
    'fdr',
    'fwe'
]

recursive_eliminate = [
    RFE,
    RFECV,
]

methods = [
    GenericUnivariateSelect,  # 0
    RFE,
    RFECV,
    VarianceThreshold,  # 2
    SelectFromModel,
]


# methodology and type for later use.
def feature_selection(dataset, label, mode=0, param=2, methodology=0, type=0, estimator=None, timeout=0):
    # features_size = features.shape[1]
    # data = dataset[1:, :-features_size]
    # label = dataset[1:, -features_size:]
    data = dataset

    # Selection
    selection_dataset = {}
    for selection in selections:
        if selection not in selection_dataset.keys():
            selection_dataset[selection] = {}
        transformer = GenericUnivariateSelect(chi2, selection, param=param)
        print(data.shape)
        selection_dataset[selection]['data'] = transformer.fit_transform(data, label)
        print(selection_dataset[selection]['data'].shape)
        selection_dataset[selection]['feature'] = transformer.get_support()

    print("selection")

    # Recursive Elimination
    re_dataset = {}
    if estimator is not None:
        for re in recursive_eliminate:
            if re.__name__ not in re_dataset.keys():
                re_dataset[re.__name__] = {}
            selector = re(estimator, param)
            re_dataset[re.__name__]['data'] = selector.fit_transform(data, label)
            re_dataset[re.__name__]['feature'] = selector.get_support()

    print("re el")

    # Threshold
    threshold_dataset = {}
    selector = VarianceThreshold()
    threshold_dataset['data'] = selector.fit_transform(data, label)
    threshold_dataset['feature'] = selector.get_support()

    # Model Adaption
    model_dataset = {}

    return selection_dataset, re_dataset, threshold_dataset, model_dataset


if __name__ == '__main__':
    iris = load_iris()
    pass
