"""
Базовый класс для HTTP клиентов
"""
from typing import Any, Dict, Optional
from urllib.parse import urljoin
from app.infrastructure.http.interfaces import IHttpClient


class BaseHttpClient(IHttpClient):
    """Базовый класс для HTTP клиентов с общей логикой"""

    def __init__(
        self,
        base_url: str = "",
        default_headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0
    ):
        self._base_url = base_url.rstrip("/")
        self._default_headers = default_headers or {}
        self._timeout = timeout

    def _build_url(self, path: str) -> str:
        """Построить полный URL"""
        if path.startswith(("http://", "https://")):
            return path
        return urljoin(f"{self._base_url}/", path.lstrip("/"))

    def _merge_headers(
        self,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """Объединить дефолтные и переданные заголовки"""
        result = self._default_headers.copy()
        if headers:
            result.update(headers)
        return result

    def _get_timeout(self, timeout: Optional[float] = None) -> float:
        """Получить таймаут"""
        return timeout if timeout is not None else self._timeout
