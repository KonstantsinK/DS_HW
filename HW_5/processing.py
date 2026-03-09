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


