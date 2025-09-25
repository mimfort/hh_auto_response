"""
Bot Runner - запуск бота (без инициализации БД)
"""
import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from app.di import get_container



async def main():
    """Главная функция запуска бота (без инициализации БД)"""
    # Настраиваем логирование
    logging.basicConfig(level=logging.INFO)
    
    # Красивый вывод
    print("\n💼 HH.ru Auto-Apply Bot")
    print("==================================================")
    print("🚀 Автоматизация откликов на вакансии hh.ru...")
    print("🏗️ Архитектура: Microservices + Clean Architecture")
    print("📊 Структура: Domain → Application → Infrastructure → Adapters")
    print("🎯 Функции: Поиск вакансий | Массовые отклики | Аналитика")
    
    try:
        # ✅ Убрали инициализацию БД
        # Предполагается, что БД уже настроена и таблицы созданы
        
        print("📦 Инициализация telegram-gateway сервиса...")
        container = get_container()
        print("🔧 Настройка Telegram API (удаление webhook)...")
        await container.bot.delete_webhook(drop_pending_updates=True)
        
        # Создаем Dispatcher с FSM storage
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        print("🔄 Настройка middleware для межсервисного взаимодействия...")
        # Добавляем middleware для автоматического управления сессиями
        from app.adapters.middleware import DatabaseMiddleware
        dp.message.middleware(DatabaseMiddleware(container))
        dp.callback_query.middleware(DatabaseMiddleware(container))
        
        print("🎛️ Регистрация обработчиков команд и callback'ов...")
        # Создаем обработчики без сессии (используют middleware)
        handlers = container.get_handlers()
        # Регистрируем роутер
        dp.include_router(handlers.router)
        

        
        # Запускаем бота с сессионным middleware
        print("✅ Telegram Gateway готов к работе!")
        print("� Начинаю обработку сообщений от пользователей...")
        print("==================================================")
        await dp.start_polling(container.bot)
    except Exception as e:
        print(f"❌ Ошибка запуска Telegram Gateway: {str(e)}")
        logging.exception("Критическая ошибка при запуске микросервиса:")
    finally:
        # Закрываем соединения
        if 'container' in locals() and hasattr(container, 'bot'):
            await container.bot.session.close()
            print("👋 Telegram Gateway остановлен, соединения закрыты")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n� HH Auto-Apply Bot остановлен пользователем (Ctrl+C)")
    except Exception as e:
        print(f"\n💥 Критическая ошибка telegram-gateway сервиса: {str(e)}")
        logging.exception("Необработанная ошибка микросервиса:")