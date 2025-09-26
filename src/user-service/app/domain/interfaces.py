"""
IUserRepository interface - контракт для репозитория пользователей
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_active_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> Optional[User]:
        pass

    @abstractmethod
    def _model_to_domain(self, model) -> User:
        """Преобразует ORM модель в доменную модель"""
        pass

    @abstractmethod
    def _domain_to_model(self, domain: User):
        """Преобразует доменную модель в ORM модель"""
        pass


class IUserService(ABC):
    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def register_user(
        self,
        tg_id: int,
        username: Optional[str],
        first_name: str,
        last_name: Optional[str],
        language_code: Optional[str],
    ) -> User:
        pass
