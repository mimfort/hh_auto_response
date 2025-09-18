from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class IPaginationInfo:
    """Информация о пагинации"""
    current_page: int
    total_pages: int
    items_per_page: int
    total_items: int
    start_item: int
    end_item: int
    has_previous: bool
    has_next: bool

class IPaginationService(ABC):
    """Интерфейс для сервиса пагинации"""

    @abstractmethod
    def paginate(self, items: list, page: int, items_per_page: int) -> tuple[list, IPaginationInfo]:
        """Пагинация списка элементов"""
        pass

class ITelegramMessageSender(ABC):
    """Интерфейс для отправки сообщений через Telegram"""

    @abstractmethod
    async def send_message(self, response) -> None:
        """Отправляет сообщение через Telegram API"""
        pass

    @abstractmethod
    async def edit_message(self, response) -> None:
        """Редактирует сообщение через Telegram API"""
        pass


class ITelegramBotInfoProvider(ABC):
    """Интерфейс для получения информации о боте"""

    @abstractmethod
    async def get_bot_username(self) -> str:
        """Возвращает username бота"""
        pass