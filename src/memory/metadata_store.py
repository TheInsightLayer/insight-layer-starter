
import sqlite3

class MetadataStore:
    def __init__(self, db_path="data/memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    who TEXT, what TEXT, when TEXT,
                    why TEXT, how TEXT, outcome TEXT, source TEXT
                )
            """)

    def save(self, insight: dict):
        with self.conn:
            self.conn.execute("""
                INSERT INTO insights (who, what, when, why, how, outcome, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                insight["who"], insight["what"], insight["when"],
                insight["why"], insight["how"], insight["outcome"], insight.get("source")
            ))
