# models/Magazine.py
from database.connection import get_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self._name = name
        self._category = category
        self._create_magazine()

    def _create_magazine(self):
        # Insert a new magazine into the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)', 
                       (self.id, self._name, self._category))
        conn.commit()
        conn.close()

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def articles(self):
        # Get all articles in the magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    @property
    def contributors(self):
        # Get all authors who have written for the magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DISTINCT a.* FROM authors a
        JOIN articles ar ON a.id = ar.author_id
        WHERE ar.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    @property
    def article_titles(self):
        # Get titles of all articles in the magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title[0] for title in titles]

    @property
    def contributing_authors(self):
        # Get authors with more than 2 articles in the magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT a.*, COUNT(ar.id) as article_count FROM authors a
        JOIN articles ar ON a.id = ar.author_id
        WHERE ar.magazine_id = ?
        GROUP BY a.id
        HAVING article_count > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors if authors else None
