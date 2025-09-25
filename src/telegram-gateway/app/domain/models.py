"""
Domain models - бизнес-сущности на Pydantic
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, computed_field

class User(BaseModel):
    """Пользователь бота"""
    id: int|None = None  # ID пользователя в базе данных
    tg_id: int
    username: str|None
    first_name: str
    last_name: str|None
    language_code: str|None
    is_banned: bool = False
    is_admin: bool = False
    
  
    @computed_field
    @property
    def full_name(self) -> str:
        """Полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.username or f"User{self.tg_id}"


class Message(BaseModel):
    """Сообщение от пользователя"""
    id: int
    user: User
    text: Optional[str] = None
    timestamp: datetime
    chat_id: int


class BotResponse(BaseModel):
    """Ответ бота"""
    chat_id: int
    text: str
    reply_markup: Optional[Dict[str, Any]] = None
    parse_mode: str|None = "HTML"
    message_id: int | None = None  