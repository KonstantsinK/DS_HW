#data_processing
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from statsmodels.tsa.stattools import adfuller
def info(df):
  #Информация о датасете
    return df.info()
def count_missing(df):
    # Количество пропущенных значений в каждом столбце.
    return df.isnull().sum().sort_values(ascending=False)
def missing_report(df):
    #Отчёт о пропущенных значениях
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100
    report = pd.DataFrame({
        'Пропущено': missing_count,
        'Процент': missing_percent
    })
    report = report[report['Пропущено'] > 0].sort_values('Пропущено', ascending=False)
    return report
def head(df):
    print('\n Первые пять строк набора данных')
    return df.head()
# Типы данных и пропущенные значения
def date_type(df):
    print("\n Типы данных и пропущенные значения:")
    info_df = pd.DataFrame({
        "Data Type": df.dtypes,
        "Missing values": df.isnull().sum(),
        "Missing %": (df.isnull().sum()/len(df)*100).round(2),
        "Unique Values": df.nunique()
    })
    return info_df
# Разделение значений на категориальные и числовые
def classify_variables(df):
    categorical = []
    numerical = []
    for col in df.columns:
        if df[col].dtype == 'object':
            categorical.append(col)
        elif df[col].dtype in ['int64','float64']:
            if df[col].nunique() < 10:
                categorical.append(col)
            else:
                numerical.append(col)

    return categorical, numerical

def Encoding(df):
    #Преобразование категориальных данных в бинарные
    # идентификация категориальных данных для которых тип данных 'object'
    categorical_variables = df.columns[df.dtypes == 'object']
    #конвертация в бинарные данные Истина-Ложь
    df = pd.get_dummies(df,columns=categorical_variables,drop_first=True)
    # Конвертация Истина-Ложь в 0/1
    df = df.astype(int)
    return df
def remove_outliers(df, column):
    percentile25 = df[column].quantile(0.25)
    percentile75 = df[column].quantile(0.75)
    iqr = percentile75-percentile25
    upper_limit = percentile75 + 1.5 * iqr
    lower_limit = percentile25 - 1.5 * iqr
    df = df[(df[column] < upper_limit) & (df[column] > lower_limit)]
    return df
# #Преобразование колонки с датой в формат datetime
def datetime(data):
    data['date'] = pd.to_datetime(data['date']).dt.tz_localize(None)

    data['date'] = data['date'].dt.to_period('M').dt.to_timestamp()

    # Устанавливаем индекс и задаем частоту 'MS' (Month Start)
    data.set_index('date', inplace=True)
    data = data.asfreq('MS')
    #Проверка на разрывы
    if data['price'].isnull().any():
        print("Внимание: пропущены целые месяцы! Заполняем...")
        data['price'] = data['price'].interpolate() # Линейная интерполяция
    # Сортировка (критически важно для временных рядов!)
    data.sort_index(inplace=True)
    return data
#Тест на стационарность (Тест Дики-Фуллера)
def testDF(data):
    result = adfuller(data['price'])
    print(f'ADF Statistic: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')
    # Главное правило интерпретации:
    if result[1] <= 0.05:
        print("Ряд стационарен")
    else:
        print("Ряд нестационарен (требуется дифференцирование)")

#Автоматическое определение d
def check_stationarity(series):
    result = adfuller(series.dropna())
    return result[1] # возвращаем p-value
def autoD(data):
    # Исходный ряд
    p_val = check_stationarity(data['price'])
    d = 0

    print(f"Исходный p-value: {p_val:.4f}")

    #   Цикл дифференцирования
    temp_series = data['price'].copy()
    while p_val > 0.05 and d < 2: # Обычно d не превышает 2
        d += 1
        temp_series = temp_series.diff().dropna()
        p_val = check_stationarity(temp_series)
        print(f"После {d}-го порядка дифференцирования p-value: {p_val:.4f}")

    if p_val <= 0.05:
        print(f"\nРяд стал стационарным. Рекомендуемый параметр d = {d}")
    else:
        print(f"\nРяд всё еще нестационарен. Возможно, нужны логарифмы или учет сезонности (D).")
