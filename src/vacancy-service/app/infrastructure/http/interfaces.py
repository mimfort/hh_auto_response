"""
Интерфейсы для HTTP клиентов
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin


class IHttpClient(ABC):
    """Интерфейс для HTTP клиента"""
    
    @abstractmethod
    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """GET запрос"""
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """POST запрос"""
        pass

    @abstractmethod
    async def put(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """PUT запрос"""
        pass

    @abstractmethod
    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """DELETE запрос"""
        pass
