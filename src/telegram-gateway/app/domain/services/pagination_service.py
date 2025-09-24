"""
Pagination Service - сервис пагинации
"""
from typing import List, TypeVar, Generic, Dict, Any
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class PaginationInfo:
    """Информация о пагинации"""
    current_page: int
    total_pages: int
    items_per_page: int
    total_items: int
    start_item: int
    end_item: int
    has_previous: bool
    has_next: bool


class PaginationService(Generic[T]):
    """Сервис для работы с пагинацией"""
    
    def calculate_pagination(
        self, 
        items: List[T], 
        page: int = 0, 
        items_per_page: int = 5
    ) -> tuple[List[T], PaginationInfo]:
        """
        Рассчитывает пагинацию для списка элементов
        
        Args:
            items: Список элементов для пагинации
            page: Номер страницы (начиная с 0)
            items_per_page: Количество элементов на странице
            
        Returns:
            Кортеж (элементы_страницы, информация_о_пагинации)
        """
        total_items = len(items)
        total_pages = (total_items + items_per_page - 1) // items_per_page if total_items > 0 else 1
        
        # Валидация номера страницы
        page = max(0, min(page, total_pages - 1))
        
        # Вычисляем границы
        start_idx = page * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        
        # Получаем элементы для текущей страницы
        page_items = items[start_idx:end_idx]
        
        # Создаем информацию о пагинации
        pagination_info = PaginationInfo(
            current_page=page,
            total_pages=total_pages,
            items_per_page=items_per_page,
            total_items=total_items,
            start_item=start_idx + 1 if total_items > 0 else 0,
            end_item=end_idx,
            has_previous=page > 0,
            has_next=page < total_pages - 1
        )
        
        return page_items, pagination_info
    
    def build_navigation_buttons(
        self, 
        pagination_info: PaginationInfo, 
        callback_prefix: str,
    ) -> List[Dict[str, str]]:
        """
        Строит кнопки навигации для пагинации
        
        Args:
            pagination_info: Информация о пагинации
            callback_prefix: Префикс для callback_data (например, "admin_cities")
            
        Returns:
            Список кнопок для инлайн клавиатуры
        """
        navigation_buttons = []
        
        # Кнопка "Предыдущая"
        if pagination_info.has_previous:
            navigation_buttons.append({
                "text": "⬅️ Пред.",
                "callback_data": f"{callback_prefix}_page_{pagination_info.current_page - 1}"
            })
        
        # Информационная кнопка
        if pagination_info.total_pages > 1:
            navigation_buttons.append({
                "text": f"📄 {pagination_info.current_page + 1}/{pagination_info.total_pages}",
                "callback_data": f"{callback_prefix}_info"
            })
        
        # Кнопка "Следующая"
        if pagination_info.has_next:
            navigation_buttons.append({
                "text": "След. ➡️",
                "callback_data": f"{callback_prefix}_page_{pagination_info.current_page + 1}"
            })
        
        return navigation_buttons
    
    def format_pagination_text(
        self, 
        pagination_info: PaginationInfo, 
        entity_name: str = "элементов"
    ) -> str:
        """
        Форматирует текст с информацией о пагинации
        
        Args:
            pagination_info: Информация о пагинации
            entity_name: Название сущности во множественном числе (например, "городов", "домов")
            
        Returns:
            Отформатированный текст
        """
        if pagination_info.total_items == 0:
            return f"❌ <b>Нет доступных {entity_name}</b>"
        
        text = f"📄 Страница {pagination_info.current_page + 1} из {pagination_info.total_pages}\n"
        text += f"📊 Показано {pagination_info.start_item}-{pagination_info.end_item} из {pagination_info.total_items} {entity_name}"
        
        return text
