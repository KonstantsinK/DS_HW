#data_processing
import pandas as pd
from sklearn.preprocessing import LabelEncoder

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

def InfoClass(df):
    #Суммарные данные о классах
    return df.booking_status.value_counts()
def EncodingClass(df):
    le = LabelEncoder()
    df.booking_status = le.fit_transform(df.booking_status)
    return df.booking_status.value_counts()

