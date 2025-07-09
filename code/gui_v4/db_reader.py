# db_reader.py
import yaml
import json
import os
from pathlib import Path

class DBReader:
    def __init__(self, db_path="code/db.yaml"):
        self.db_path = Path(db_path)
        
    def get_keys(self):
        if not self.db_path.exists():
            return []
            
        with self.db_path.open('r') as f:
            data = yaml.safe_load(f) or {}
        return list(data.keys())
    
    def get_data(self, key: str):
        if not self.db_path.exists():
            return {}
            
        with self.db_path.open('r') as f:
            data = yaml.safe_load(f) or {}
        return data.get(key, {})
    
    def connect_to_db(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(cur_dir)
        target_folder = "db"
        target_path = os.path.join(parent_dir, target_folder)

        if os.path.exists(target_path) and os.path.isdir(target_path):
            print(f"✅ Папка '{target_folder}' найдена по пути: {target_path}")
            with os.scandir(target_path) as entries:
                folder_contents = {}
                with os.scandir(target_path) as entries:
                    for entry in entries:
                        if entry.is_dir():
                            folder_contents[entry.name] = [
                                item.name for item in os.scandir(entry.path)
                            ]
                print(folder_contents)
        else:
            print(f"❌ Папка '{target_folder}' отсутствует в директории: {parent_dir}")
        
    def read_json_db(self):
        with open('code/db.json', 'r') as json_file:
            db_json = json.load(json_file)
            print(db_json.keys())


if __name__ == '__main__':
    dbr = DBReader()
    dbr.read_json_db()