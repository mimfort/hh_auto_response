"""
Application services for UI operations.
"""
from app.application.interfaces import (
    IMessageFormattingService,
    IBotInfoProvider,
    IPaginationService
)
from app.application.interfaces import IBotUIService


class BotUIService(IBotUIService):
    def __init__(
            self,
            message_formatter:IMessageFormattingService,
            bot_info_provider:IBotInfoProvider,
            pagination_service:IPaginationService,
    ):
        self.message_formatter = message_formatter
        self.bot_info_provider = bot_info_provider
        self.pagination_service = pagination_service

    def _build_main_menu_keyboard(self):
        # Логика построения главного меню
        pass