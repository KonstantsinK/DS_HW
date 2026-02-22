#data_loader
import csv
import os
import sqlite3
def load_to_sql(filepath: str):
  conn = sqlite3.connect('medical_data.db')
  cursor = conn.cursor()
  # Создание таблицы Medical
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Medical (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      Age INTEGER, Gender INTEGER, Heart INTEGER,
      "Systolic blood pressure" INTEGER,
      "Diastolic blood pressure" INTEGER,
      "Blood sugar" REAL, "CK-MB" REAL,
       Troponin REAL, Result TEXT
       )
    ''')
  with open(filepath, 'r') as f:
    reader = csv.DictReader(f)
    # Список ключей (заголовков) в том порядке, в котором они идут в CSV
    keys = [
        'Age', 'Gender', 'Heart rate',
        'Systolic blood pressure', 'Diastolic blood pressure',
        'Blood sugar', 'CK-MB', 'Troponin', 'Result'
     ]
    # Каждый словарь переводим в кортеж значений в нужном порядке
    # (row[key] гарантирует, что мы берем верные данные, даже если в CSV другой порядок)
    data_to_insert = (tuple(row[k] for k in keys) for row in reader)
    # Формирование запроса sql
    sql = 'INSERT INTO Medical (Age, Gender, Heart, "Systolic blood pressure", "Diastolic blood pressure", "Blood sugar", "CK-MB", Troponin, Result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    # Попытка выполнить запрос
    try:
        cursor.executemany(sql, data_to_insert)
        conn.commit()
        print("Готово! Загрузка данных в базу завершена.")
    except Exception as e:
        print(f"Ошибка: {e}")

  conn.close()