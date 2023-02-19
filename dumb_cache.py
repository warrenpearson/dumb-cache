import json
import os
import sqlite3
from pathlib import Path


class DumbCache:
    def __init__(self):
        self._cache_path = None

    def set_cache_path(self, path):
        if path.startswith("/"):
            self._cache_path = path
        else:
            here = os.path.dirname(os.path.realpath(__file__))
            self._cache_path = f"{here}/{path}"

    def default_cache_path(self):
        here = os.path.dirname(os.path.realpath(__file__))
        return f"{here}/cache.sqlite3"

    def get_cache_path(self):
        if self._cache_path is None:
            self._cache_path = self.default_cache_path()

        return self._cache_path

    def make_cache(self):
        conn = sqlite3.connect(self.get_cache_path())
        c = conn.cursor()

        c.execute("DROP TABLE IF EXISTS cache_data")
        c.execute("CREATE TABLE cache_data(key text unique, data json)")
        conn.commit()
        conn.close()

    def set_cache_data(self, key, data):
        cache_path = Path(self.get_cache_path())
        if not cache_path.is_file():
            self.make_cache()

        conn = sqlite3.connect(cache_path)
        c = conn.cursor()
        values = (key, json.dumps(data), json.dumps(data))

        statement = """INSERT INTO cache_data (key, data) VALUES(?, ?)
                       ON CONFLICT(key) DO UPDATE SET data=?"""

        c.execute(statement, values)
        conn.commit()
        conn.close()

    def get_cache_data(self, key):
        cache_path = Path(self.get_cache_path())
        if not cache_path.is_file():
            return None

        conn = sqlite3.connect(cache_path)
        cur = conn.cursor()
        params = [key]
        cur.execute("select data from cache_data where key = ?", params)
        r = cur.fetchone()
        return json.loads(r[0])

    def update_cache_data(self, key, data):
        self.set_cache_data(key, data)
