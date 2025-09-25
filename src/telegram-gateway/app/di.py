'''
Dependency Injection Container - собираем все зависимости приложения
'''
from app.config import Settings
from aiogram import Bot
from app.application.services.ui_service import BotUIService
from app.domain.services.message_formatting_service import MessageFormattingService
from app.adapters.telegram import TelegramMessageSender, TelegramBotInfoProvider
from app.domain.services.pagination_service import PaginationService
from app.application.use_cases import BotUseCases
from app.adapters.handlers import TelegramHandlers

class Container:
    def __init__(self):
        self.config = Settings()
        self.bot = Bot(token=self.config.TELEGRAM_BOT_TOKEN)

        #TODO: Добавить доступ к микросервису user-service
        
        #TODO: Добавить доменные сервисы
        self.message_formatter=MessageFormattingService()
        self.pagination_service=PaginationService()


        #Создаем адаптеры (без состояния)
        self.bot_info_provider=TelegramBotInfoProvider(self.bot)
        self.message_sender=TelegramMessageSender(self.bot)



    async def get_ui_service(self) -> BotUIService:
        """Создает UI сервис"""
        return BotUIService(
            message_formatter=self.message_formatter,
            bot_info_provider=self.bot_info_provider,
            pagination_service=self.pagination_service
        )
    

#TODO: Добавление получения репозиториев и сервисов

    async def get_use_cases(self) -> BotUseCases:
        """Создает use cases с зависимостями"""
        # Получаем сервисы через новые методы
        # user_service = await self.get_user_service(session)
        ui_service = await self.get_ui_service()
        
        # Создаем use cases
        return BotUseCases(
            message_sender=self.message_sender,
            bot_info_provider=self.bot_info_provider,
            # user_service=user_service,
            ui_service=ui_service,

        )
#TODO: Добавление хендлеров
    def get_handlers(self) -> TelegramHandlers:
        """Создает обработчики без use cases (они будут из middleware)"""
        return TelegramHandlers()

# Глобальный контейнер
_container: Container = None


def get_container() -> Container:
    """Получает глобальный экземпляр контейнера"""
    global _container
    if _container is None:
        _container = Container()
    return _container