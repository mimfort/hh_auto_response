from typing import Optional, List
from app.domain.interfaces import IUserService, IUserRepository
from app.domain.models import User
from app.domain.exceptions import UserAlreadyExistsError, UserNotFoundError


class UserService(IUserService):
    """Сервис для работы с пользователями (бизнес-логика)"""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def get_user(self, user_id: int) -> User:
        """Получить пользователя по ID"""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        return await self._user_repository.get_by_telegram_id(telegram_id)

    async def create_user(self, telegram_id: int, **kwargs) -> User:
        """Создать нового пользователя"""
        if await self.get_by_telegram_id(telegram_id):
            raise UserAlreadyExistsError(
                f"User with telegram_id {telegram_id} already exists"
            )

        user = User(telegram_id=telegram_id, **kwargs)
        return await self._user_repository.create(user)

    async def update_user(self, user_id: int, **kwargs) -> User:
        """Обновить данные пользователя"""
        user = await self.get_user(user_id)  # Вызовет UserNotFoundError если нет

        for key, value in kwargs.items():
            setattr(user, key, value)

        return await self._user_repository.update(user)

    async def ban_user(self, user_id: int) -> User:
        """Забанить пользователя"""
        user = await self.get_user(user_id)  # Вызовет UserNotFoundError если нет
        user.ban()
        return await self._user_repository.update(user)

    async def get_active_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Получить список активных пользователей"""
        return await self._user_repository.get_active_users(limit, offset)
