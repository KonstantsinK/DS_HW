#data_query
import sqlite3
#Выполнение запроса к базе sql
def execute_query(dbase, query:str):
  connection = sqlite3.connect(dbase)
  cursor = connection.cursor()
  result = None
  try:
        cursor.execute(query)
        if cursor.description:
           headers = [col[0] for col in cursor.description]
        else:
           print("Запрос не вернул столбцов")
        result = cursor.fetchall()
  except Exception as e:
        print(f"Ошибка: {e}")
  connection.close()
  return result, headers