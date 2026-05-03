from models.database import Database

class Controller:
    def __init__(self):
        self.db = Database()

    def get_books(self):
        return self.db.get_books()

    def add_book(self, data):
        self.db.add_book(data)

    def update_book(self, book_id, data):
        self.db.update_book(book_id, data)

    def delete_book(self, book_id):
        self.db.delete_book(book_id)