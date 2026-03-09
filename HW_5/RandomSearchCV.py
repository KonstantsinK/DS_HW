#Автоматический подбор гиперпараметров моделей МО путем случайного поиска.
import hyperparam as hp
import warnings
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
def best_parametr(X_train, y_train):
    warnings.filterwarnings("ignore")
    tree_params, gradient_params, light_params, knn_params, rf_params, adaboost_params = hp.list_hypar()
    randomcv_models = [
        ("KNN", KNeighborsRegressor(), knn_params),
        ("Random", RandomForestRegressor(), rf_params),
        ("Adaboost", AdaBoostRegressor(), adaboost_params),
        ("Gradient", GradientBoostingRegressor(), gradient_params),
        ("Light", LGBMRegressor(verbosity=-1), light_params),
        ("Tree", DecisionTreeRegressor(), tree_params)
        ]
    best_param = {}
    best_models = {}
    for name, model, params in randomcv_models:
        randomcv = RandomizedSearchCV(estimator=model, param_distributions=params, cv=5, n_jobs=-1, n_iter=6)
        randomcv.fit(X_train, y_train)
        best_models[name] = randomcv.best_estimator_
    return best_models
#Возвращает словарь улучшенных моделей


