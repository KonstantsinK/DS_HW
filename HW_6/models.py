from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from sklearn.model_selection import train_test_split
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
def modelSarima(data):
    ts = data['price']
    # Создаем и обучаем модель SARIMA
    model_sarima = SARIMAX(ts, order=(4, 1, 3), seasonal_order=(4, 1, 3, 12))  # Пример параметров (p, d, q) и (P, D, Q, s)
    results_sarima = model_sarima.fit()
    # Визуализируем прогноз
    plt.figure(figsize=(12, 6))
    plt.plot(ts, label='Исходные данные')
    plt.plot(results_sarima.fittedvalues, color='red', label='Прогноз (SARIMA)')
    plt.title("Цена нефти с использованием SARIMA")
    plt.xlabel("Месяц")
    plt.ylabel("Цена")
    plt.legend()
    plt.show()
    return results_sarima
def predSarima (results_sarima, data, step): #Прогноз по обученной модели SARIMA
    # Прогноз на 3 шага (месяца) вперед

    forecast_obj = results_sarima.get_forecast(steps=step)

    # Извлекаем средние значения прогноза
    forecast_mean = forecast_obj.predicted_mean

    # Извлекаем доверительные интервалы (по умолчанию 95%)
    conf_int = forecast_obj.conf_int()

    # Создание дат для прогноза
    last_date = data.index[-1]
    #pd.to_datetime(data['date']).iloc[-1]
    #data.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=step, freq='MS')
    forecast_mean.index = forecast_dates
    conf_int.index = forecast_dates

    # Вывод таблицы
    forecast_df = pd.concat([forecast_mean, conf_int], axis=1)
    forecast_df.columns = ['Прогноз', 'Нижняя граница', 'Верхняя граница']
    print("ПРОГНОЗ SARIMA:")
    print(forecast_df.round(2))

    # Визуализация
    plt.figure(figsize=(10, 5))
    plt.plot(data['price'][-12:], label='История (12 мес)', marker='o')
    plt.plot(forecast_mean, label='Прогноз SARIMA', color='red', marker='s', linestyle='--')

    # Закрашиваем зону неопределенности
    plt.fill_between(forecast_dates,
                 conf_int.iloc[:, 0],
                 conf_int.iloc[:, 1], color='pink', alpha=0.3, label='Доверительный интервал')

    plt.title('Прогноз SARIMA ')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
    
#Auto-ARIMA
def model_autoArima(data):
    import pmdarima as pm
    model_auto = pm.auto_arima(data['price'],
                           seasonal=False, 
                           stepwise=True,
                           suppress_warnings=True,
                           error_action="ignore",
                           max_p=3, max_q=3, # Ограничим поиск для скорости
                           trace=True) # Покажет процесс подбора в консоли

    print(f"Лучшие подобранные параметры: {model_auto.order} x {model_auto.seasonal_order}")
    
    # Обучение (автоматический подбор параметров)
    model_arima = pm.ARIMA(order=model_auto.order)
    
    results_arima = model_arima.fit(data['price'])
    # Визуализируем прогноз
    plt.figure(figsize=(12, 6))
    plt.plot(data['price'], label='Исходные данные')
    plt.plot(results_arima.predict_in_sample(), color='red', label='Прогноз (ARIMA)')
    plt.title("Цена нефти с использованием ARIMA")
    plt.xlabel("Месяц")
    plt.ylabel("Цена")
    plt.legend()
    plt.show()
    print(model_auto.summary())
    

    return model_auto

#Прогноз по обучению auto-ARIMA
def pred_autoArima(model_auto, n_periods, data):
    #n_periods = 12
    forecast, conf_int = model_auto.predict(n_periods=n_periods, return_conf_int=True)

    # Создание дат для будущего периода
    last_date = data.index[-1]
    forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1),
                               periods=n_periods, freq='MS')

    # Визуализация результата
    plt.figure(figsize=(18, 6))
    plt.plot(data['price'][-12:], label='История', color='blue')
    plt.plot(forecast_index, forecast, label='Авто-прогноз', color='green', marker='o')

    #Доверительный интервал (зона риска)
    plt.fill_between(forecast_index, conf_int[:, 0], conf_int[:, 1], color='green', alpha=0.15)

    plt.title('Прогноз с использованием Auto-ARIMA')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    return forecast, conf_int, forecast_index

# Модель Холта-Уинтерса
from statsmodels.tsa.holtwinters import ExponentialSmoothing
def model_hw(data):
    model_hw = ExponentialSmoothing(data['price'],
                                trend='add',
                                seasonal='add',
                                seasonal_periods=12).fit()

    # Визуализируем прогноз
    plt.figure(figsize=(12, 6))
    plt.plot(data['price'], label='Исходные данные')
    plt.plot(model_hw.fittedvalues, color='red', label='Прогноз (Холта-Уинтерса')
    plt.title("Цена нефти с использованием метода Холта-Уинтерса")
    plt.xlabel("Месяц")
    plt.ylabel("Цена")
    plt.legend()
    plt.show()
    return model_hw
#
def pred_modelHW(model_hw, data, period):
    forecast_3m = model_hw.forecast(3)

    # Создание дат для прогноза (следующие 3 месяца от последней точки данных)
    last_date = data.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=period, freq='MS')
    forecast_series = pd.Series(forecast_3m.values, index=forecast_dates)

    # Вывод точных цифр
    print("ПРОГНОЗ ХОЛТА-УИНТЕРСА НА КВАРТАЛ:")
    print(pd.DataFrame({'Прогноз': forecast_series}).round(2))

    # Визуализация: соединяем историю и будущее
    plt.figure(figsize=(10, 5))
    plt.plot(data['price'][-12:], label='История (последний год)', marker='o', color='blue')
    plt.plot(forecast_series, label='Прогноз HW (3 мес)', color='green', marker='s', linestyle='--')

    # Линия-связка между последней точкой истории и первой точкой прогноза
    plt.plot([data.index[-1], forecast_series.index[0]],
            [data['price'].iloc[-1], forecast_series.iloc[0]], color='green', linestyle='--')

    plt.title('Краткосрочный прогноз: Метод Холта-Уинтерса')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Расчет метрик точности SARIMA
def metricaSARIMA(data):
    from sklearn.metrics import mean_absolute_error

    # Подготовка данных
    history = list(data['price'][:-12]) # Начинаем с обучающей выборки
    test = data['price'][-12:]          # Проверяем на последних 12 месяцах
    predictions = []
    model = SARIMAX(history, order=(4, 1, 3), seasonal_order=(4, 1, 3, 12), error_action="ignore", enforce_stationarity=False, enforce_invertibility=False)  
    model_fit = model.fit(disp=False) # Сначала сохраняем результат обучения
    print("Запуск скользящего прогноза (это может занять время)...")
    current_model_fit = model_fit
    # Цикл скользящего прогноза
    for i in range(len(test)):
        # Обучаем модель на всей доступной на данный момент истории

         yhat = current_model_fit.forecast(steps=1)
         predictions.append(yhat.iloc[0])
        
        # Получаем новое реальное значение
         new_observation = test.iloc[[i]] 
        
        # Добавляем данные в модель БЕЗ переобучения параметров
        # refit=False — это ключ к скорости
         current_model_fit = current_model_fit.append(new_observation, refit=False)

         print(f"Месяц {i+1}/12: Предсказано={yhat:.2f}, Реально={test.iloc[i]:.2f}")

    # Оценка точности
    rolling_mae = mean_absolute_error(test, predictions)
    print(f"\nСредняя ошибка (MAE) скользящего прогноза: {rolling_mae:.2f}")

    # Визуализация
    plt.figure(figsize=(18, 6))
    plt.plot(test.index, test, label='Реальные цены (Test)', marker='o', color='blue')
    plt.plot(test.index, predictions, label='Rolling Forecast', marker='x', color='red', linestyle='--')

    plt.title('Проверка модели: Прогноз на 1 шаг вперед с переобучением')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Метрики Холта-Уинтерса
def metricaHW(df):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from sklearn.metrics import mean_absolute_percentage_error
    from sklearn.metrics import mean_absolute_error
    # 1. Подготовка 
    history = list(df['price'][:-12])
    test = df['price'][-12:]
    predictions = []

    # 2. Цикл скользящего прогноза
    for t in range(len(test)):
        # Обучаем модель Холта-Уинтерса на текущей истории
        # trend='add', seasonal='add' — стандарт для линейных данных
        model = ExponentialSmoothing(history, trend='add', seasonal='add', seasonal_periods=12)
        model_fit = model.fit()
        
        # Предсказываем 1 следующий шаг
        yhat = model_fit.forecast(steps=1)
        predictions.append(yhat[0])
        
        # Добавляем реальное значение в историю для следующего шага
        history.append(test.iloc[t])
        print(f"Месяц {t+1}/12: Предсказано={yhat:.2f}, Реально={test.iloc[t]:.2f}")

    # Оценка точности
    rolling_mae = mean_absolute_error(test, predictions)
    print(f"\nСредняя ошибка (MAE) скользящего прогноза: {rolling_mae:.2f}")

    # Визуализация
    plt.figure(figsize=(18, 6))
    plt.plot(test.index, test, label='Реальные цены (Test)', marker='o', color='blue')
    plt.plot(test.index, predictions, label='Rolling Forecast', marker='x', color='red', linestyle='--')

    plt.title('Проверка модели: Прогноз на 1 шаг вперед с переобучением')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    