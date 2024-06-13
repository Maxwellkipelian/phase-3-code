# models/Author.py
from database.connection import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self._name = name
        self._create_author()
    
    def _create_author(self):
        # Insert a new author into the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (id, name) VALUES (?, ?)', (self.id, self._name))
        conn.commit()
        conn.close()

    @property
    def name(self):
        return self._name

    @property
    def articles(self):
        # Get all articles written by the author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    @property
    def magazines(self):
        # Get all magazines the author has written for
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DISTINCT m.* FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines
