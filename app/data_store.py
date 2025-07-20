import sqlite3
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataStore:
    def __init__(self, db_path="osint.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            date DATETIME,
            url TEXT,
            source TEXT,
            category TEXT,
            locations TEXT
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def store_article(self, article_data):
        query = """
        INSERT INTO articles (title, text, date, url, source, category, locations)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            article_data['title'],
            article_data['text'],
            article_data['date'],
            article_data['url'],
            article_data['source'],
            article_data['category'],
            json.dumps(article_data['locations'])
        ))
        self.conn.commit()

    def fetch_articles(self, category=None, date_range=None):
        query = "SELECT * FROM articles"
        conditions = []
        params = []
        if category:
            conditions.append("category = ?")
            params.append(category)
        if date_range:
            conditions.append("date >= ? AND date <= ?")
            params.extend(date_range)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
