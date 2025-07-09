import dearpygui.dearpygui as dpg
import json
from pathlib import Path
import os

class DBReader:
    def __init__(self, db_path=None):
        if db_path is None:
            # Автоматическое определение пути к db.json
            current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = current_dir / "db.json"
        else:
            self.db_path = Path(db_path)
        print(f"Using DB at: {self.db_path.absolute()}")

    def get_keys(self):
        """Возвращает ключи верхнего уровня из JSON"""
        if not self.db_path.exists():
            print(f"DB file not found: {self.db_path}")
            return []
            
        try:
            with self.db_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                return list(data.keys())
        except Exception as e:
            print(f"Error reading DB: {e}")
            return []

    def get_data(self, key: str):
        """Возвращает данные по выбранному ключу"""
        if not self.db_path.exists():
            return {}
            
        try:
            with self.db_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get(key, {})
        except Exception as e:
            print(f"Error reading DB: {e}")
            return {}
