from abc import ABC, abstractmethod
from typing import Any, Dict

class IBotInfoProvider(ABC):
    """Интерфейс для получения информации о боте"""
    
    @abstractmethod
    async def get_bot_username(self) -> str:
        """Возвращает username бота"""
        pass

class IMessageFormattingService(ABC):
    """Интерфейс для форматирования сообщений"""


    @abstractmethod
    def _wrap_text(self, text: str) -> str:
        """Интерфейс для переноса длинных строк для соответствия ширине"""
        pass

    @abstractmethod
    def _add_consistent_width(self, text: str) -> str:
        """Интерфейс для добавления унифицированной ширины к сообщению"""
        pass

    @abstractmethod
    def format_welcome_message(self, user_first_name: str) -> str:
        """Интерфейс для форматирования приветственного сообщения"""
        pass

