import os
import unittest

from bin.book import Book, EBookStatus
from bin.errors import BookIdNotExistException, BookAlreadyThisStatusException
from bin.library import Library

book_title = "Название"
book_author = "Автор Т. Т."
book_year = 2000

file_name = "test-data.json"
library: Library
test_book: Book


class TestLibrary(unittest.TestCase):
    """Класс для тестирования функционала библиотеки"""

    def tearDown(self):
        """Метод для удаления файла библиотеки после запуска всех тестов"""

        global library
        library.delete_data()

    def test_add_book(self):
        """Метод для тестирования добавления книги в библиотеку"""

        global library, test_book, file_name
        library = Library(file_name)

        test_book = library.add_book(book_title, book_author, book_year)

        self.assertEqual(test_book.status, EBookStatus.IN_STOCK)
        self.assertEqual(test_book.title, book_title)
        self.assertEqual(test_book.author, book_author)
        self.assertEqual(test_book.year, book_year)

        books = library.books
        self.assertEqual(len(books), 1)
        self.assertEqual(test_book, books[0])

        library.add_book(book_title, book_author, book_year)
        library.add_book(book_title, book_author, book_year)
        self.assertEqual(len(books), 3)

    def test_del_book(self):
        """Метод для тестирования удаления книги из библиотеки"""

        global library, test_book
        with self.assertRaises(BookIdNotExistException):
            library.del_book("")

        count = 0
        for book in library.books:
            if book.id == test_book.id:
                count += 1
        self.assertEqual(count, 1)

        library.del_book(test_book.id)

        count = 0
        for book in library.books:
            if book.id == test_book.id:
                count += 1
        self.assertEqual(count, 0)

    def test_search(self):
        """Метод для тестирования поиска книги из библиотеки"""

        global library
        new_author = "Автор1 Т. Т."
        new_year = 2001
        library.add_book(book_title, new_author, book_year)
        library.add_book(book_title, new_author, new_year)

        self.assertEqual(len(library.search_books(author="Автор")), 4)
        self.assertEqual(len(library.search_books(author="Автор1")), 2)
        self.assertEqual(len(library.search_books(title=book_title)), 4)
        self.assertEqual(len(library.search_books(year=book_year)), 3)

    def test_change_status(self):
        """Метод для тестирования изменения статуса книги"""

        global library
        with self.assertRaises(BookIdNotExistException):
            library.change_status("", EBookStatus.CHECKED_OUT)

        book = library.add_book(book_title, book_author, book_year)
        with self.assertRaises(BookAlreadyThisStatusException):
            library.change_status(book.id, EBookStatus.IN_STOCK)

        library.change_status(book.id, EBookStatus.CHECKED_OUT)
        changed_book = library.del_book(book.id)
        self.assertEqual(changed_book.status, EBookStatus.CHECKED_OUT)


if __name__ == '__main__':
    unittest.main()
