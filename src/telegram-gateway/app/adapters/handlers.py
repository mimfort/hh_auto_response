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


    async def start_command(
        self,
        message: Message,
        use_cases: BotUseCases,
        state: FSMContext
    ):
        """Обработчик команды /start"""
        await state.clear()
        user = User(
            tg_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code
        )
        await use_cases.handle_start_command(user, message.chat.id)