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
    def format_message(self, template: str, context: Dict[str, Any]) -> str:
        pass


