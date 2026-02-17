#data loader
import pandas as pd
import requests
def load_csv(filepath: str):

    try:
        df = pd.read_csv(filepath)
        print(f"CSV файл {filepath} загружен.")
        return df
    except Exception as e:
        print(f"Ошибка при загрузке CSV: {e}")
        return None
def load_api_url(url: str):
     try:
        responce = requests.get(url)
        responce.raise_for_status()
        data = responce.json()
        print(f"Данные из API {url} загружены.")
        return pd.DataFrame(data)
     except Exception as e:
        print(f"Ошибка при загрузке из API: {e}")
        return None