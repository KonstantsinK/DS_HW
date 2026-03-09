from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from lightgbm import LGBMRegressor
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
# Расчет метрик
def evaluate_model(true, predicted):
    mae = mean_absolute_error(true, predicted)
    mse = mean_squared_error(true, predicted)
    rmse = np.sqrt(mean_squared_error(true, predicted))
    r2_square = r2_score(true, predicted)
    return mae, rmse, r2_square
# Список моделей
models = {
    "K Neighbors Regressor" : KNeighborsRegressor(),
    "Decision Tree" : DecisionTreeRegressor(),
    "Random Forest Regressor" : RandomForestRegressor(),
    "Adaboost Regressor" : AdaBoostRegressor(),
    "Gradient Boost Regressor" : GradientBoostingRegressor(),
    "LightGBM": LGBMRegressor(verbosity=-1)
}

def train_model(X_train, X_test, y_train, y_test):
    #Обучаем каждую модель из списка и расчитываем для нее метрики
    for i in range(len(list(models))):
        model = list(models.values())[i]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae, rmse, r2_square = evaluate_model(y_test, y_pred)
        print(list(models.keys())[i],"\n")
        print("Model Performance")
        print("Mean Absolute Error: ", mae)
        print("Root Mean Squared Error: ", rmse)
        print("R2 Score: ", r2_square)
        print("-----------------------------------")
        print("\n")

def train_best_models(best_models, X_train, X_test, y_train, y_test):
    result_rmse = {}
    result_r2 = {}
    for i in range(len(list(best_models))):
        model = list(best_models.values())[i]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae, rmse, r2_square = evaluate_model(y_test, y_pred)
        result_rmse[list(best_models.keys())[i]] = rmse
        result_r2[list(best_models.keys())[i]] = r2_square

        print(list(best_models.keys())[i],"\n")
        print("Производительность модели")
        print("Mean Absolute Error: ", mae)
        print("Root Mean Squared Error: ", rmse)
        print("R2 Score: ", r2_square)
        plt.figure(figsize=(6,6))
        plt.scatter(y_test, y_pred, alpha=0.6, color='blue', edgecolor='k')
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Actual vs Predicted")
        plt.grid(True)
        plt.show()
        print("\n")
        print("-----------------------------------")
    return result_rmse, result_r2
