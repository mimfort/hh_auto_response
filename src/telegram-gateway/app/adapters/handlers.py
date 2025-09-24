"""
Telegram Handlers - обработчики для Telegram
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.domain.models import User
from app.application.use_cases import BotUseCases
#TODO: Добавить состояния


class TelegramHandlers:
    """Обработчики для Telegram"""
    
    def __init__(self):
        """Инициализация роутера и регистрация обработчиков"""
        self.router = Router(name="telegram_handlers")
        self._register_handlers()
    
    def _register_handlers(self):
        # Команды 
        self.router.message.register(self.start_command, Command("start"))

        #TODO: Добавить состояния


        #TODO: Добавить обработчик инлайн кнопок (колбеки)
        