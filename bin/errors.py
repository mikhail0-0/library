class LibraryException(Exception):
    pass

class BookIdNotExistException(LibraryException):
    def __str__(self) -> str:
        return "Книги с таким id нет в библиотеке"


class BookAlreadyThisStatusException(LibraryException):
    def __str__(self) -> str:
        return "Книга уже имеет указанный статус"


class WrongFileContentException(LibraryException):
    def __str__(self) -> str:
        return "Неправильное содержимое файла"


class WrongStatusException(LibraryException):
    def __init__(self, bad_status: str):
        self.__bad_status = bad_status

    def __str__(self) -> str:
        return f"Введен неправильный статус: {self.__bad_status}"
