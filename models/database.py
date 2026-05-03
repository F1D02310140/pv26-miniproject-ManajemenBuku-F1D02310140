import sqlite3
import os


class Database:
    def __init__(self):
        os.makedirs("database", exist_ok=True)
        self.conn = sqlite3.connect("database/books.db")
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            genre TEXT NOT NULL,
            status TEXT CHECK(status IN ('Belum Dibaca', 'Sedang Dibaca', 'Selesai')) NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5) NOT NULL
        )
        """)
        self.conn.commit()

    def add_book(self, data):
        try:
            self.conn.execute(
                "INSERT INTO books (judul, penulis, genre, status, rating) VALUES (?, ?, ?, ?, ?)",
                data
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error saat menambah data:", e)

    def get_books(self):
        cursor = self.conn.execute("SELECT * FROM books ORDER BY id DESC")
        return cursor.fetchall()

    def update_book(self, book_id, data):
        try:
            self.conn.execute("""
            UPDATE books 
            SET judul=?, penulis=?, genre=?, status=?, rating=? 
            WHERE id=?
            """, (*data, book_id))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error saat update data:", e)

    def delete_book(self, book_id):
        self.conn.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()

    def __del__(self):
        if self.conn:
            self.conn.close()