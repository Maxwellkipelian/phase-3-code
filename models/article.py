# models/Article.py
from database.connection import get_connection

class Article:
    def __init__(self, author, magazine, title):
        self.author_id = author.id
        self.magazine_id = magazine.id
        self._title = title
        self._create_article()

    def _create_article(self):
        # Insert a new article into the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)', 
                       (self.author_id, self.magazine_id, self._title))
        conn.commit()
        conn.close()

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        # Get the author of the article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author = cursor.fetchone()
        conn.close()
        return author

    @property
    def magazine(self):
        # Get the magazine of the article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return magazine
