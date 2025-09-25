from app.application.interfaces import (
    ITelegramMessageSender,
    IBotInfoProvider,
    IBotUIService    
)
from app.domain.models import User





class BotUseCases:
    """Контейнер для всех use cases бота"""
    def __init__(
        self,
        message_sender: ITelegramMessageSender,
        bot_info_provider: IBotInfoProvider,
        # user_service: IUserService,
        ui_service: IBotUIService,
    ):
        self.message_sender = message_sender
        self.bot_info_provider = bot_info_provider
        #self.user_service = user_service
        self.ui_service = ui_service

    async def handle_start_command(self, user_data:User, chat_id:int):
        """Обрабатывает команду /start"""
        #user = await self.user_service.get_or_create_user(user_data)


        response = self.ui_service.create_welcome_response(user_data, chat_id)  # Позже будем использовать user, как выстроим user-service
        await self.message_sender.send_message(response)