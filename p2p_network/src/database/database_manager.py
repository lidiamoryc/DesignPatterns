import json


class DatabaseManager():
    def __init__(self, db_path, model_type):
        self.db_path = db_path
        self.model_type = model_type
        self.db = None
        self.start_db()
        

    def start_db(self):
        self.db = {
        "model_type": self.model_type,
        "combinations": []}
        self.write_db()

    def read_db(self):
        with open(self.db_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_db(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=4)

    def add_to_db(self, data: dict):
        self.db["combinations"].append((data))
        self.write_db()