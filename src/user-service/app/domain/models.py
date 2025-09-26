"""
Domain models для User Service
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    """Пользователь бота"""

    id: int | None = None  # ID пользователя в базе данных
    tg_id: int
    username: str | None
    first_name: str
    last_name: str | None
    language_code: str | None
    is_banned: bool = False
    is_admin: bool = False

    def ban(self):
        """Забанить пользователя"""
        self.is_banned = True
