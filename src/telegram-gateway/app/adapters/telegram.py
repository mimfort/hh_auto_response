"""
Telegram adapters - адаптеры для работы с Telegram API
"""
from typing import Optional
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from app.application.interfaces import ITelegramMessageSender, ITelegramBotInfoProvider
from app.domain.models import BotResponse


class TelegramMessageSender(ITelegramMessageSender):
    """Адаптер для отправки сообщений через Telegram"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def send_message(self, response: BotResponse) -> None:
        """Отправляет сообщение через Telegram API"""
        reply_markup = None
        if response.reply_markup:
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=response.reply_markup["inline_keyboard"]
            )
        
        await self.bot.send_message(
            chat_id=response.chat_id,
            text=response.text,
            parse_mode=response.parse_mode,
            reply_markup=reply_markup
        )
    async def edit_message(self, response: BotResponse) -> None:
        """Редактирует сообщение через aiogram"""
        reply_markup = None
        if response.reply_markup:
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=response.reply_markup["inline_keyboard"]
            )
        
        await self.bot.edit_message_text(
            chat_id=response.chat_id,
            message_id=response.message_id,  # Предполагаем, что message_id есть в response
            text=response.text,
            parse_mode=response.parse_mode,
            reply_markup=reply_markup
        )


class TelegramBotInfoProvider(ITelegramBotInfoProvider):
    """Адаптер для получения информации о боте"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self._cached_username: Optional[str] = None
    
    async def get_bot_username(self) -> str:
        """Возвращает username бота"""
        if self._cached_username is None:
            me = await self.bot.get_me()
            self._cached_username = me.username or "unknown"
        return self._cached_username
