from typing import Any


class DomainError(Exception):
    """Базовый класс для всех доменных исключений"""

    def __init__(self, message: str, details: Any = None):
        self.message = message
        self.details = details
        super().__init__(message)


class UserError(DomainError):
    """Базовый класс для ошибок, связанных с пользователями"""

    pass


class UserNotFoundError(UserError):
    """Пользователь не найден"""

    pass


class UserAlreadyExistsError(UserError):
    """Пользователь уже существует"""

    pass


class UserBanError(UserError):
    """Ошибка при бане пользователя"""

    pass


class ValidationError(DomainError):
    """Ошибка валидации данных"""

    pass
