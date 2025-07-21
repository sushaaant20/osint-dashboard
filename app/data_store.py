import sqlite3
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataStore:
    def __init__(self, db_path="osint.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Create a new SQLite connection and cursor."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=True)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database {self.db_path}: {e}")
            raise RuntimeError(f"Database connection failed: {e}")

    def create_table(self):
        """Create articles table if it doesn't exist."""
        if self.cursor is None or self.conn is None:
            logger.error("No database connection. Call _connect() first.")
            raise RuntimeError("No database connection available")
        try:
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
        except sqlite3.Error as e:
            logger.error(f"Error creating table: {e}")
            raise

    def store_article(self, article_data):
        """Store an article in the database."""
        query = """
        INSERT INTO articles (title, text, date, url, source, category, locations)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self.db_path, check_same_thread=True) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    article_data['title'],
                    article_data['text'],
                    article_data['date'],
                    article_data['url'],
                    article_data['source'],
                    article_data['category'],
                    json.dumps(article_data['locations'])
                ))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error storing article: {e}")

    def fetch_articles(self, category=None, date_range=None):
        """Fetch articles with optional filters."""
        try:
            with sqlite3.connect(self.db_path, check_same_thread=True) as conn:
                cursor = conn.cursor()
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
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error fetching articles: {e}")
            return []

    def close(self):
        """Explicitly close the connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            logger.error(f"Error closing database connection: {e}")
        finally:
            self.cursor = None
            self.conn = None
