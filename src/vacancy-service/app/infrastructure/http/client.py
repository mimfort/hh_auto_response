"""
HTTPX реализация HTTP клиента
"""
from typing import Any, Dict, Optional, Union
import httpx
from app.infrastructure.http.base import BaseHttpClient


class HttpxClient(BaseHttpClient):
    """Реализация HTTP клиента на базе HTTPX"""

    def __init__(
        self,
        base_url: str = "",
        default_headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True
    ):
        super().__init__(base_url, default_headers, timeout)
        self._client = httpx.AsyncClient(
            verify=verify_ssl,
            timeout=timeout,
            follow_redirects=True
        )

    async def __aenter__(self):
        """Поддержка контекстного менеджера"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрыть клиент при выходе из контекста"""
        await self._client.aclose()

    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """GET запрос"""
        response = await self._client.get(
            self._build_url(url),
            params=params,
            headers=self._merge_headers(headers),
            timeout=self._get_timeout(timeout)
        )
        response.raise_for_status()
        return response.json()

    async def post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """POST запрос"""
        response = await self._client.post(
            self._build_url(url),
            json=json,
            content=data,
            headers=self._merge_headers(headers),
            timeout=self._get_timeout(timeout)
        )
        response.raise_for_status()
        return response.json()

    async def put(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """PUT запрос"""
        response = await self._client.put(
            self._build_url(url),
            json=json,
            content=data,
            headers=self._merge_headers(headers),
            timeout=self._get_timeout(timeout)
        )
        response.raise_for_status()
        return response.json()

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """DELETE запрос"""
        response = await self._client.delete(
            self._build_url(url),
            headers=self._merge_headers(headers),
            timeout=self._get_timeout(timeout)
        )
        response.raise_for_status()
        return response.json()
        
    async def close(self):
        """Закрыть клиент"""
        await self._client.aclose()
