"""
Database Middleware - управление сессиями БД
"""
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.di import Container


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для автоматического управления сессиями БД"""
    
    def __init__(self, container: Container):
        super().__init__()
        self.container = container
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Добавляем use_cases в data для handlers и dialogs
        use_cases = await self.container.get_use_cases()
        data["use_cases"] = use_cases
            
        # Добавляем для aiogram-dialog middleware_data
        if "middleware_data" not in data:
            data["middleware_data"] = {}
        data["middleware_data"]["use_cases"] = use_cases

        # Вызываем обработчик с данными
        return await handler(event, data)
