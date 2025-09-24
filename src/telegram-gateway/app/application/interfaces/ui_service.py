"""
Интерфейс для UI сервиса бота
"""
from app.application.interfaces import (
    IMessageFormattingService,
    IBotInfoProvider,
    IPaginationService
)

class IBotUIService:
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