'''
Dependency Injection Container - собираем все зависимости приложения
'''
from config import config
from aiogram import Bot
from app.application.services.ui_service import BotUIService
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
class Container:
    def __init__(self):
        self.config = config
        self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        
        #Создаем доменные сервисы (без состояния)
        #TODO: Добавить доменные сервисы
        self.message_formatter=self.message_formatter, 
        self.bot_info_provider=self.bot_info_provider,
        self.pagination_service=self.pagination_service


        #Создаем адаптеры (без состояния)
        #TODO: Добавить адаптеры


    async def get_ui_service(self) -> BotUIService:
        """Создает UI сервис"""
        return BotUIService(
            message_formatter=self.message_formatter,
            bot_info_provider=self.bot_info_provider,
            pagination_service=self.pagination_service
        )

#TODO: Добавление получения репозиториев и сервисов

    async def get_use_cases(self, session: AsyncSession) -> BotUseCases:
        """Создает use cases с зависимостями"""
        # Получаем сервисы через новые методы
        # user_service = await self.get_user_service(session)
        # user_repository = await self.get_user_repository(session)
        # ui_service = await self.get_ui_service()
        
        # Создаем use cases
        return BotUseCases(
            # message_sender=self.message_sender,
            # user_repository=user_repository,
            # bot_info_provider=self.bot_info_provider,
            # user_service=user_service,
            # ui_service=ui_service,

        )
    

# Глобальный контейнер
_container: Container = None


def get_container() -> Container:
    """Получает глобальный экземпляр контейнера"""
    global _container
    if _container is None:
        _container = Container(config)
    return _container