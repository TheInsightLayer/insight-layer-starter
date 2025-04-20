import sqlite3
from pathlib import Path

DB_PATH = Path("data/insights.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS insights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        insight TEXT,
        tags TEXT,
        related_to TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_insights(insights):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in insights:
        c.execute("""
        INSERT INTO insights (source, insight, tags, related_to, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (
            item['source'],
            item['insight'],
            ','.join(item['tags']),
            ','.join(item['related_to']),
            item['timestamp']
        ))
    conn.commit()
    conn.close()

def search_insights(keyword=None, tag=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = "SELECT * FROM insights WHERE 1=1"
    params = []
    if keyword:
        query += " AND insight LIKE ?"
        params.append(f"%{keyword}%")
    if tag:
        query += " AND tags LIKE ?"
        params.append(f"%{tag}%")
    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    return results

def replace_insight(index, new_item):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    UPDATE insights SET
        source = ?,
        insight = ?,
        tags = ?,
        related_to = ?,
        timestamp = ?
    WHERE id = ?
    """, (
        new_item['source'],
        new_item['insight'],
        ','.join(new_item['tags']),
        ','.join(new_item['related_to']),
        new_item['timestamp'],
        index
    ))
    conn.commit()
    conn.close()