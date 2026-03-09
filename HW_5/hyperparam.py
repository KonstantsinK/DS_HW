#Списки гиперпараметров
def list_hypar():
# Функция возвращает списки гиперпараметров для каждой модели
    tree_params = {
    "criterion": ["squared_error", "absolute_error"],
    "splitter": ["best", "random"],
    "max_depth": [5,15,20,None],
    "max_features": ["sqrt", "log2", None]
    }

    gradient_params = {
    "n_estimators": [100,150,200],
    "max_depth": [3,4,5],
    "loss": ["squared_error", "absoluet_error", "huber", "quantile"],
    "learning_rate": [0.01, 0.1, 0.5]
     }
    light_params = {
    "n_estimators": [100,200,300],
    "learning_rate": [0.01,0.1],
    "num_leaves": [31, 50, 70],
    "max_depth": [-1, 5, 10],
    "min_child_samples": [10,20,30],
    "subsample": [0.6,0.8,1.0],
    "colsample_bytree": [0.6,0.8,1.0]
     }

    knn_params = {"n_neighbors": [2,3,10,20,40,50]}

    rf_params = {
    "max_depth": [5,8,10,15,None],
    "max_features": ["sqrt", "log2", 5, 7, 10],
    "min_samples_split": [2, 8, 12, 20],
    "n_estimators": [100, 200, 500, 1000]
    }

    adaboost_params = {
    "n_estimators": [50,80,100,120],
    "learning_rate": [0.001, 0.01, 0.1, 1.0, 2.0],
    "loss": ["linear", "square", "exponential"]
    }
    return tree_params, gradient_params, light_params, knn_params, rf_params, adaboost_params