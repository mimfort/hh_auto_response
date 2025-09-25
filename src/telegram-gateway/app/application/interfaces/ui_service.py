"""
Интерфейс для UI сервиса бота
"""
from app.application.interfaces import (
    IMessageFormattingService,
    IBotInfoProvider,
    IPaginationService
)
from abc import ABC, abstractmethod
from app.domain.models import BotResponse
class IBotUIService(ABC):
    """Интерфейс для UI сервиса бота"""
    def __init__(
        self,
        message_formatter: IMessageFormattingService,
        bot_info_provider: IBotInfoProvider,
        pagination_service: IPaginationService
    ):
        self.message_formatter = message_formatter
        self.bot_info_provider = bot_info_provider
        self.pagination_service = pagination_service
    @abstractmethod
    def create_welcome_response(self, user, chat_id: int) -> BotResponse:
        """Создает приветственное сообщение с основным меню"""
        pass
