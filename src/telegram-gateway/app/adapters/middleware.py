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
    
