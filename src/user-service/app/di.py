"""
Dependency Injection контейнер для user-service
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import get_settings
from app.domain.interfaces import IUserRepository, IUserService
from app.domain.services.user_service import UserService



class Container:
    """DI контейнер для user-service"""

    def __init__(self):
        self._settings = get_settings()

        # Database
        self._engine = create_async_engine(
            self._settings.DATABASE_URL, echo=self._settings.MODE == "DEV"
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,  # Для лучшего контроля над транзакциями
        )

        # Repositories
        self._user_repository: IUserRepository | None = None

        # Services
        self._user_service: IUserService | None = None

        # Use Cases
        self._create_user_use_case: CreateUserUseCase | None = None
        self._get_user_use_case: GetUserUseCase | None = None
        self._update_user_use_case: UpdateUserUseCase | None = None
        self._delete_user_use_case: DeleteUserUseCase | None = None
        self._ban_user_use_case: BanUserUseCase | None = None

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получить сессию базы данных"""
        async with self._session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    async def user_repository(self) -> IUserRepository:
        """Получить репозиторий пользователей"""
        if not self._user_repository:
            session = await anext(self.session())
            self._user_repository = UserRepository(session)
        return self._user_repository

    async def user_service(self) -> IUserService:
        """Получить сервис пользователей"""
        if not self._user_service:
            repository = await self.user_repository()
            self._user_service = UserService(repository)
        return self._user_service

    async def create_user_use_case(self) -> CreateUserUseCase:
        """Получить use case создания пользователя"""
        if not self._create_user_use_case:
            service = await self.user_service()
            self._create_user_use_case = CreateUserUseCase(service)
        return self._create_user_use_case

    async def get_user_use_case(self) -> GetUserUseCase:
        """Получить use case получения пользователя"""
        if not self._get_user_use_case:
            service = await self.user_service()
            self._get_user_use_case = GetUserUseCase(service)
        return self._get_user_use_case

    async def update_user_use_case(self) -> UpdateUserUseCase:
        """Получить use case обновления пользователя"""
        if not self._update_user_use_case:
            service = await self.user_service()
            self._update_user_use_case = UpdateUserUseCase(service)
        return self._update_user_use_case

    async def delete_user_use_case(self) -> DeleteUserUseCase:
        """Получить use case удаления пользователя"""
        if not self._delete_user_use_case:
            service = await self.user_service()
            self._delete_user_use_case = DeleteUserUseCase(service)
        return self._delete_user_use_case

    async def ban_user_use_case(self) -> BanUserUseCase:
        """Получить use case бана пользователя"""
        if not self._ban_user_use_case:
            service = await self.user_service()
            self._ban_user_use_case = BanUserUseCase(service)
        return self._ban_user_use_case


# Глобальный контейнер
_container: Container | None = None


def get_container() -> Container:
    """Получить глобальный контейнер"""
    global _container
    if _container is None:
        _container = Container()
    return _container


# FastAPI dependencies
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency для получения сессии БД"""
    async for session in get_container().session():
        yield session


async def get_user_repository() -> IUserRepository:
    """FastAPI dependency для получения репозитория пользователей"""
    return await get_container().user_repository()


async def get_user_service() -> IUserService:
    """FastAPI dependency для получения сервиса пользователей"""
    return await get_container().user_service()


async def get_create_user_use_case() -> CreateUserUseCase:
    """FastAPI dependency для получения use case создания пользователя"""
    return await get_container().create_user_use_case()


async def get_get_user_use_case() -> GetUserUseCase:
    """FastAPI dependency для получения use case получения пользователя"""
    return await get_container().get_user_use_case()


async def get_update_user_use_case() -> UpdateUserUseCase:
    """FastAPI dependency для получения use case обновления пользователя"""
    return await get_container().update_user_use_case()


async def get_delete_user_use_case() -> DeleteUserUseCase:
    """FastAPI dependency для получения use case удаления пользователя"""
    return await get_container().delete_user_use_case()


async def get_ban_user_use_case() -> BanUserUseCase:
    """FastAPI dependency для получения use case бана пользователя"""
    return await get_container().ban_user_use_case()
