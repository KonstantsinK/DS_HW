#data_processing
import pandas as pd
import sqlite3
from sklearn.preprocessing import LabelEncoder

#Получение дата-фрейма из запроса sql
def prepare_date(dbase, query):
  connection = sqlite3.connect(dbase)
  df = pd.read_sql(query, connection)
  connection.close()
  return df

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

#data_processing
import pandas as pd
import sqlite3
from sklearn.preprocessing import LabelEncoder

#Получение дата-фрейма из запроса sql
def prepare_date(dbase, query):
  connection = sqlite3.connect(dbase)
  df = pd.read_sql(query, connection)
  connection.close()
  return df

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
    return df.Result.value_counts()
def EncodingClass(df):
    le = LabelEncoder()
    df.Result = le.fit_transform(df.Result)
    return df.Result.value_counts()



