from dataclasses import dataclass
from enum import Enum, unique


@unique
class EBookStatus(str, Enum):
    """Enum класс для хранения статуса книги"""

    IN_STOCK: str = "IN_STOCK"
    CHECKED_OUT: str = "CHECKED_OUT"


@dataclass
class Book:
    """Класс для хранения информации о книге"""

    id: str
    """id в uuid формате"""
    status: EBookStatus
    """статус IN_STOCK - в наличии, CHECKED_OUT - выдана"""
    title: str
    """название"""
    author: str
    """автор"""
    year: int
    """год издания"""

    @staticmethod
    def show(books: list['Book']):
        """Статический метод для отображения списка книг в виде таблицы"""

        if len(books) == 0:
            print(books)
            return

        dicts = [book.__dict__ for book in books]
        max_sizes: dict[str, int] = dict()

        for book in dicts:
            for key in book:
                val_len = len(str(book[key]))
                if key not in max_sizes:
                    max_sizes[key] = len(key)
                if max_sizes[key] < val_len:
                    max_sizes[key] = val_len

        sep = " | "

        total_len = 0
        for key in books[0].__dict__:
            total_len += max_sizes[key] + len(sep)
            print(key + " " * (max_sizes[key] - len(key)), end=sep)
        print()
        print("-" * total_len)

        for book in dicts:
            for key in book:
                print(str(book[key]) + " " * (max_sizes[key] - len(str(book[key]))), end=sep)
            print()
