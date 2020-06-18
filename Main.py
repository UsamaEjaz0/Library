import pickle

import sqlite3

from datetime import date

conn = sqlite3.connect('books.db')


class Book:
    title = None
    author = None
    category = None

    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category

    def __str__(self):
        return "Name: {}, Author: {}, Category: {}".format(self.title, self.author, self.category)


# Receipt class
#
# Class to generate the receipt
class Receipt:
    books = []

    def add_book(self, book: Book, due_date=date.today()):
        self.books.append([book, due_date])

    def remove_book(self, book: Book):
        self.books.remove(book)

    def generate_receipt(self):
        print("Receipt")
        for book, due_date in self.books:
            print(book)
            print("Due date: ", due_date)


class Library:
    filename = "data.bin"
    books = []
    borrowed = []

    def __init__(self):
        self.load()

    def add_book(self, book: Book):
        self.books.append(book)
        self.save()
        pass

    def search_book_by_name(self, name):
        cursor = conn.cursor();
        print("RESULTS FROM MySql DATABASE:")
        query = "SELECT * FROM `books` WHERE title='" + name + "'"
        cursor.execute(query)
        print(cursor.fetchall())
        conn.commit()
        # conn.close()

        print("RESULTS FROM File-based DATABASE:")

        result = []
        for book in self.books:
            if book.title == name:
                result.append(book)
        self.print_book_list(result)
        return result

    def search_book_by_author(self, author):
        print("RESULTS FROM MySql DATABASE:")
        cursor = conn.cursor();
        query = "SELECT * FROM `books` WHERE author='" + author + "'"
        cursor.execute(query)
        print(cursor.fetchall())
        conn.commit()
        # conn.close()

        print("RESULTS FROM File-based DATABASE:")
        result = []
        for book in self.books:
            if book.author == author:
                result.append(book)
        self.print_book_list(result)
        return result

    def search_book_by_category(self, category):
        print("RESULTS FROM MySql DATABASE:")
        cursor = conn.cursor();
        query = "SELECT * FROM `books` WHERE category='" + category + "'"
        cursor.execute(query)
        print(cursor.fetchall())
        conn.commit()
        # conn.close()

        print("RESULTS FROM File-based DATABASE:")
        result = []
        for book in self.books:
            if book.category == category:
                result.append(book)
        self.print_book_list(result)
        return result

    def save(self):
        pickle.dump(self, open(self.filename, "bw"))

    def load(self):
        try:
            lib = pickle.load(open(self.filename, "br"))
            self.books = lib.books
            self.borrowed = lib.borrowed
            pass
        except IOError:
            pass

    def print_book_list(self, lst):
        for book in lst:
            pass


class UI:
    lib = Library()
    receipt = Receipt()

    def __init__(self):
        pass

    def add_book_prompt(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        cat = input("Enter category: ")
        self.lib.add_book(Book(title, author, cat))

        cursor = conn.cursor();
        query = "INSERT INTO `books`(`title`, `author`, `category`) VALUES ('" + title + "','" + author + "','" + cat + "')"
        cursor.execute(query)
        conn.commit()
        # conn.close()

    def search(self):
        param = input("Enter a string to search for: ")
        result = Menu(["Search by name", "Search by author", "Search by category"],
                      [self.lib.search_book_by_name, self.lib.search_book_by_author, self.lib.search_book_by_category],
                      [param]).show()

        if len(result) > 0:
            for i, book in zip(range(1, len(result) + 1), result):
                print(i, ". ", book, sep='')
            op = input('Do you want to add book to bucket [Y/n]: ')
            if op != 'n':
                self.receipt.add_book(result[int(input('Enter book number: ')) - 1])

    def print_receipt(self):
        self.receipt.generate_receipt()

    def show(self):
        print('Library')
        Menu(["Add to library", "Search library", "Show receipt", "Exit"],
             [self.add_book_prompt, self.search, self.print_receipt, exit]).show()
        pass


class Menu:
    menu_items = []
    menu_funcs = []
    args = []

    def __init__(self, menu_items: list, menu_funcs: list, args: list = None):
        """
        Args:
            menu_items (list):
            menu_funcs (list):
            args (list):
        """
        if len(menu_items) != len(menu_funcs):
            raise AssertionError('Size of menu items and funcs are not equal')
        self.menu_items = menu_items
        self.menu_funcs = menu_funcs
        self.args = args

    def show(self):
        size = len(self.menu_items)
        result = None
        for i, item in zip(range(size), self.menu_items):
            print('\t', i, ". ", item, sep='')

        x = int(input("Enter option: "))
        if x < size or x >= 0:
            if self.args is not None:
                result = self.menu_funcs[x](*self.args)
            else:
                result = self.menu_funcs[x]()

        return result


if __name__ == "__main__":
    ui = UI()
    while True:
        ui.show()
