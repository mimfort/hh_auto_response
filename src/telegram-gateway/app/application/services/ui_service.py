from app.domain.models import BotResponse, User
from app.application.interfaces import (
    IMessageFormattingService,
    IBotInfoProvider,
    IPaginationService,
    IBotUIService
)

class BotUIService(IBotUIService):
    def __init__(
        self,
        message_formatter: IMessageFormattingService,
        bot_info_provider: IBotInfoProvider,
        pagination_service: IPaginationService,
    ):
        self.message_formatter = message_formatter
        self.bot_info_provider = bot_info_provider
        self.pagination_service = pagination_service

    def create_welcome_response(self, user: User, chat_id: int) -> BotResponse:
        """Создает приветственное сообщение с основным меню"""
        welcome_text = self.message_formatter.format_welcome_message(user.first_name)
        
        # Создаем клавиатуру главного меню
        main_menu_keyboard = self._build_main_menu_keyboard()
        
        # ✅ ВОЗВРАЩАЕМ BotResponse, а не tuple!
        return BotResponse(
            chat_id=chat_id,
            text=welcome_text,
            reply_markup=main_menu_keyboard,
            parse_mode="HTML"
        )

    def _build_main_menu_keyboard(self) -> dict:
        """Строит клавиатуру главного меню"""
        return {
            "inline_keyboard": [
                [
                    {"text": "🔍 Поиск вакансий", "callback_data": "search_vacancies"},
                    {"text": "⚙️ Настройки", "callback_data": "settings"}
                ],
                [
                    {"text": "📊 Мои отклики", "callback_data": "my_applications"},
                    {"text": "📈 Статистика", "callback_data": "analytics"}
                ],
                [
                    {"text": "👤 Профиль", "callback_data": "profile"},
                    {"text": "❓ Помощь", "callback_data": "help"}
                ]
            ]
        }