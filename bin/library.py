import json
import os
import uuid

from bin.book import Book, EBookStatus
from bin.errors import WrongFileContentException, BookIdNotExistException, BookAlreadyThisStatusException


class Library:
    """Класс для управления библиотекой"""

    @property
    def books(self):
        """
        Свойство для доступа к книгам библиотеки
        :return: список книг
        """

        return self.__books

    def __write(self):
        """Метод для записи текущего списка книг в файл"""

        with open(self.__file_name, "w") as file:
            dicts = [book.__dict__ for book in self.__books]
            json.dump(dicts, file, indent=2, ensure_ascii=False)

    def __init__(self, file_name="data.json"):
        self.__file_name = file_name
        if not os.path.isfile(self.__file_name):
            self.__books: list[Book] = []
            self.__write()
            return

        try:
            self.__update_books()
        except BaseException:
            raise WrongFileContentException()

    def __update_books(self):
        """Метод для получения списка книг из файла"""

        with open(self.__file_name, "r") as file:
            json_books = json.load(file)
            self.__books = [Book(**json_book) for json_book in json_books]

    def __find_book_by_id(self, book_id) -> int:
        """
        Метод для нахождения индекса книги по ее id
        :param book_id: id книги
        :return: индекс книги или -1, если книга не найдена
        """

        for i in range(len(self.__books)):
            if self.__books[i].id == book_id:
                return i

        return -1

    def delete_data(self):
        """Метод для удаления файла библиотеки"""

        os.remove(self.__file_name)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Метод для добавления книги в библиотеку
        :param title: название книги
        :param author: автор книги
        :param year: год издания книги
        :return: книга, созданная при добавлении в библиотеку
        """

        book_id = str(uuid.uuid4())
        status = EBookStatus.IN_STOCK
        new_book = Book(book_id, status, title, author, year)
        self.__books.append(new_book)
        self.__write()
        return new_book

    def del_book(self, book_id: str) -> Book:
        """
        Метод для удаления книги из библиотеки по id
        :param book_id: id книги
        :return: удаленная книга
        :raises BookIdNotExistException: Если книга не найдена
        """

        index = self.__find_book_by_id(book_id)
        if index != -1:
            pop_book = self.__books.pop(index)
            self.__write()
            return pop_book

        raise BookIdNotExistException()

    def search_books(
            self,
            title: str | None = None,
            author: str | None = None,
            year: int | None = None,
    ) -> list[Book]:
        """
        Метод для нахождения книг в библиотеке
        :param title: название книги или его часть
        :param author: имя автора книги или часть имени
        :param year: год издания книги
        :return: список книг, соответсвующих параметрам
        """

        result = []
        for book in self.__books:
            if title and title not in book.title:
                continue
            elif author and author not in book.author:
                continue
            elif year and year != book.year:
                continue
            else:
                result.append(book)

        return result

    def show(self):
        """Метод для вывода списка книг библиотеки в табличном виде"""
        Book.show(self.__books)

    def change_status(self, book_id: str, new_status: EBookStatus) -> Book:
        """
        Метод для изменения статуса книги
        :param book_id: id книги
        :param new_status: новый статус книги
        :return: книга с измененным статусом
        :raises BookIdNotExistException: Если книга не найдена
        :raises BookAlreadyThisStatusException: Если книга уже имеет статус
        """
        index = self.__find_book_by_id(book_id)
        if index == -1:
            raise BookIdNotExistException()

        book = self.__books[index]
        if book.status == new_status:
            raise BookAlreadyThisStatusException()

        book.status = new_status
        self.__write()
        return book
