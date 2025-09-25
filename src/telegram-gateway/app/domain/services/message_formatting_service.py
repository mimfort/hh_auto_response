"""
Message Formatting Service - сервис форматирования сообщений
"""
from app.application.interfaces.formatters import IMessageFormattingService

class MessageFormattingService(IMessageFormattingService):
    """Чистая бизнес-логика форматирования сообщений"""
    
    # Константы для унификации ширины интерфейса
    MAX_WIDTH = 35  # Максимальная ширина строки
    SEPARATOR_LINE = "♻️" * 20
    THIN_LINE = "" * 30
    HEADER_SEPARATOR = "♻️" * 20
    
    def _wrap_text(self, text: str) -> str:
        """Переносит длинные строки для соответствия ширине"""
        import textwrap
        lines = text.split('\n')
        wrapped_lines = []
        
        for line in lines:
            # Убираем HTML теги для подсчета ширины
            clean_line = line.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
            
            if len(clean_line) <= self.MAX_WIDTH:
                wrapped_lines.append(line)
            else:
                # Переносим длинные строки, сохраняя HTML теги
                if '<b>' in line or '<i>' in line:
                    # Для строк с HTML тегами просто добавляем как есть
                    wrapped_lines.append(line)
                else:
                    # Для обычных строк используем перенос
                    wrapped = textwrap.fill(line, width=self.MAX_WIDTH)
                    wrapped_lines.extend(wrapped.split('\n'))
        
        return '\n'.join(wrapped_lines)

    def _add_consistent_width(self, text: str) -> str:
        """Добавляет унифицированную ширину к сообщению"""
        return f"{self.THIN_LINE}\n{text}\n{self.THIN_LINE}"
    
    def format_welcome_message(self, user_first_name: str) -> str:
        """Форматирует приветственное сообщение"""
        welcome_text = (
            f"👋 Привет, <b>{user_first_name}</b>!\n\n"
            "Я - бот, который поможет тебе с поиском работы на HeadHunter.\n"
            "Используй меню ниже, чтобы начать."
        )
        welcome_text = self._wrap_text(welcome_text)
        return self._add_consistent_width(welcome_text)
    
