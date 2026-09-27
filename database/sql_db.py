import sqlite3
from core.config import settings

class SQLDatabase:
    def __init__(self):
        self.db_path = settings.SQL_DB_PATH
        self._initialize_db()

    def _initialize_db(self):
        """Creates tables and inserts mock dynamic data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_info (
                id INTEGER PRIMARY KEY,
                working_hours TEXT,
                price_per_hour REAL,
                available_spots INTEGER
            )
        ''')
        # Insert mock data if empty
        cursor.execute("SELECT COUNT(*) FROM parking_info")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO parking_info (working_hours, price_per_hour, available_spots) VALUES (?, ?, ?)",
                           ("24/7", 5.0, 42))
        conn.commit()
        conn.close()

    def get_dynamic_info(self, query: str) -> str:
        """Fetches dynamic data. In a real scenario, this would use an LLM to generate SQL."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT working_hours, price_per_hour, available_spots FROM parking_info LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            return f"Working Hours: {result[0]}, Price: ${result[1]}/hour, Available Spots: {result[2]}"
        return "No dynamic data available."