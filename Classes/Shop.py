# Copyright 2020 Артём Воронов
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3
import uuid
db_path = 'data/databases/Shop.db'


class ShopControl:
    def __init__(self, type: str = 'Weapons' or 'Armours'):
        self.type = type

    def create(self, name, stat, price):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO {self.type} VALUES("{uuid.uuid4()}", "{name}", {stat}, {price});""")
        conn.commit()
        conn.close()

    def read(self, name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"""SELECT * FROM {self.type} where name = "{name}";""").fetchone()
        conn.close()
        return result

    def set_stat(self, name, column, new):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            new = int(new)
            cursor.execute(f"""UPDATE {self.type} SET {column} = {new} where name = "{name}";""")
        except ValueError:
            cursor.execute(f"""UPDATE {self.type} SET {column} = "{new}" where name = "{name}";""")
        conn.commit()
        conn.close()

    def get_all_by_stat(self, type):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM {self.type} ORDER BY {type};").fetchall()
        conn.close()
        return result

    def remove(self, name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"""DELETE FROM {self.type} where name = "{name}";""")
        conn.commit()
        conn.close()