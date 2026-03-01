#data_loader
import pandas as pd
def load_csv(filepath: str):

    try:
        df = pd.read_csv(filepath)
        print(f"CSV файл {filepath} загружен.")
        return df
    except Exception as e:
        print(f"Ошибка при загрузке CSV: {e}")
        return None