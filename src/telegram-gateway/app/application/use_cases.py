from app.application.interfaces import (
    ITelegramMessageSender,
    IBotInfoProvider,
    

)






class BotUseCases:
    """Контейнер для всех use cases бота"""
    def __init__(
        self,
        message_sender: ITelegramMessageSender,
        user_repository: IUserRepository,
        bot_info_provider: IBotInfoProvider,
        user_service: IUserService,
        ui_service: BotUIService,
    ):
        self.message_sender = message_sender
        self.user_repository = user_repository
        self.bot_info_provider = bot_info_provider
        self.user_service = user_service
        self.ui_service = ui_service