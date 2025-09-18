'''
Dependency Injection Container - собираем все зависимости приложения
'''
from config import config
from aiogram import Bot
from app.infrastructure.database.base import async_session_maker
from app.application.services.ui_service import BotUIService
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
class Container:
    def __init__(self):
        self.config = config
        self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)

        #Прокидываем сессию
        self._session_maker = async_session_maker

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
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Создает и управляет сессией БД"""
        async with self._session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise