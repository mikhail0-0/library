import argparse
from enum import Enum, unique

from bin.book import Book, EBookStatus
from bin.errors import WrongStatusException, LibraryException
from bin.library import Library


@unique
class ECommand(str, Enum):
    add = "add"
    delete = "delete"
    search = "search"
    show = "show"
    change = "change"


parser = argparse.ArgumentParser(description="Система управления библиотекой")
subparsers = parser.add_subparsers(dest="command", required=True, help="команды")

parser_add = subparsers.add_parser(ECommand.add.value, help="добавление книги")
parser_add.add_argument("-t", dest="title", type=str, help="название книги", required=True)
parser_add.add_argument("-a", dest="author", type=str, help="автор книги", required=True)
parser_add.add_argument("-y", dest="year", type=int, help="год написания книги", required=True)

parser_delete = subparsers.add_parser(ECommand.delete.value, help="удаление книги")
parser_delete.add_argument("-i", dest="id", type=str, help="ID книги", required=True)

parser_search = subparsers.add_parser(ECommand.search.value, help="поиск книг")
parser_search.add_argument("-t", dest="title", type=str, help="название или часть названия книги")
parser_search.add_argument("-a", dest="author", type=str, help="имя автора или часть имени")
parser_search.add_argument("-y", dest="year", type=int, help="год написания книги")

parser_show = subparsers.add_parser(ECommand.show.value, help="просмотр всех книг")

parser_change = subparsers.add_parser(ECommand.change.value, help="изменение статуса книги")
parser_change.add_argument("-i", dest="id", type=str, help="ID книги", required=True)
parser_change.add_argument("-s", dest="status", type=str, help="Новый статус книги", choices=["s", "c"], required=True)

try:
    args = parser.parse_args()

    library = Library()

    match args.command:
        case ECommand.add.value:
            book = library.add_book(args.title, args.author, args.year)
            print("Следующая книга была добавлена:")
            Book.show([book])
        case ECommand.delete.value:
            book = library.del_book(args.id)
            print("Следующая книга была удалена:")
            Book.show([book])
        case ECommand.search.value:
            books = library.search_books(args.title, args.author, args.year)
            Book.show(books)
        case ECommand.show.value:
            library.show()
        case ECommand.change.value:
            status: EBookStatus
            match args.status:
                case "s":
                    status = EBookStatus.IN_STOCK
                case "c":
                    status = EBookStatus.CHECKED_OUT
                case _:
                    raise WrongStatusException(args.status)

            book = library.change_status(args.id, status)
            print("Статус книги был изменен:")
            Book.show([book])

        case _:
            print('''
                Такой команды не существует.
                Введите -h, чтобы посмотреть существующие команды
              ''')

except LibraryException as exp:
    print(exp)
except BaseException:
    print("Что-то пошло не так")
