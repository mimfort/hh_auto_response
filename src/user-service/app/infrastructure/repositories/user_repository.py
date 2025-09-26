"""
User Repository - работа с пользователями в базе данных
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from app.domain.models import User
from app.infrastructure.database.models import UserModel
from app.domain.interfaces import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session  

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        try:
            stmt = (
                select(UserModel)
                .where(UserModel.id == user_id)
                .limit(1)
            )
            result = await self._session.execute(stmt)
            user_model = result.scalar_one_or_none()
            return self._model_to_domain(user_model) if user_model else None
        except SQLAlchemyError as e:
            # Логирование ошибки
            raise ValueError(f"Error fetching user: {str(e)}")

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        try:
            stmt = (
                select(UserModel)
                .where(UserModel.telegram_id == telegram_id)
                .limit(1)
            )
            result = await self._session.execute(stmt)
            user_model = result.scalar_one_or_none()
            return self._model_to_domain(user_model) if user_model else None
        except SQLAlchemyError as e:
            raise ValueError(f"Error fetching user by telegram_id: {str(e)}")

    async def get_active_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Получить список активных пользователей"""
        try:
            stmt = (
                select(UserModel)
                .where(UserModel.is_banned == False)
                .order_by(UserModel.id)
                .limit(limit)
                .offset(offset)
            )
            result = await self._session.execute(stmt)
            users = result.scalars().all()
            return [self._model_to_domain(user) for user in users]
        except SQLAlchemyError as e:
            raise ValueError(f"Error fetching active users: {str(e)}")

    async def create(self, user: User) -> User:
        """Создать пользователя"""
        try:
            user_model = UserModel(**user.model_dump(exclude={'id'}))
            self._session.add(user_model)
            await self._session.commit()
            await self._session.refresh(user_model)
            return self._model_to_domain(user_model)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise ValueError(f"Error creating user: {str(e)}")

    async def update(self, user: User) -> Optional[User]:
        """Обновить пользователя"""
        try:
            stmt = (
                update(UserModel)
                .where(UserModel.id == user.id)
                .values(**user.model_dump(exclude={'id'}))
                .returning(UserModel)
            )
            result = await self._session.execute(stmt)
            await self._session.commit()
            updated_user = result.scalar_one_or_none()
            return self._domain_to_model(updated_user) if updated_user else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise ValueError(f"Error updating user: {str(e)}")


        

    def _model_to_domain(self, user_model: UserModel) -> User:
        """Преобразовать SQLAlchemy модель в Pydantic модель"""
        return User(
            id=user_model.id,
            tg_id=user_model.telegram_id,
            username=user_model.username,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            language_code=user_model.language_code,
            is_banned=user_model.is_banned,
            is_admin=user_model.is_admin
        )
    def _domain_to_model(self, user: User) -> UserModel:
        """Преобразовать Pydantic модель в SQLAlchemy модель"""
        return UserModel(
            id=user.id,
            telegram_id=user.tg_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
            is_banned=user.is_banned,
            is_admin=user.is_admin
        )