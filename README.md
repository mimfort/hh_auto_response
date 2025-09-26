# Telegram HH.ru Auto-Apply Bot

Бот для автоматизации откликов на вакансии hh.ru через Telegram.  
Архитектура построена по принципам **Microservices + Clean Architecture**, что обеспечивает максимальную масштабируемость, тестируемость и простоту поддержки.

---

## 🏗️ Архитектура и основные принципы

Про## 📦 Технологический стек

### Основные технологии
- **Python 3.11+** — язык программирования
- **FastAPI** — HTTP API для межсервисной коммуникации
- **aiogram** — Telegram Bot API
- **RabbitMQ** — асинхронная передача сообщений между сервисами
- **PostgreSQL** — база данных (отдельная схема для каждого сервиса)
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — миграции БД
- **pydantic** — валидация данных и моделирование
- **httpx** — HTTP-клиент для внешних API

### Инфраструктура
- **Docker & Docker Compose** — контейнеризация и оркестрация
- **Redis** — кеширование и сессии
- **nginx** — load balancer и reverse proxy
- **Prometheus + Grafana** — мониторинг
- **ELK Stack** — логирование

### Пример docker-compose.yml
```yaml
version: '3.8'
services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: hh_bot
    
  user-service:
    build: ./src/user-service
    depends_on: [postgres, rabbitmq]
    
  vacancy-service:
    build: ./src/vacancy-service
    depends_on: [postgres, rabbitmq]
    
  # ... другие сервисы
```пользует **гибридную архитектуру**:
- **Микросервисная архитектура** на верхнем уровне — разделение по доменам/функциональности
- **Clean Architecture** внутри каждого микросервиса — четкое разделение слоев

### Микросервисная архитектура
Каждый микросервис отвечает за свою область ответственности и **полностью независим**:
- **user-service** — управление пользователями, профилями, настройками
- **vacancy-service** — поиск, фильтрация и управление вакансиями
- **application-service** — логика откликов, трекинг статусов
- **notification-service** — уведомления, отчеты, аналитика
- **telegram-gateway** — точка входа, роутинг команд, UI

### Коммуникация между сервисами

Система использует **гибридный подход** для межсервисного взаимодействия. Важно понимать **когда использовать что**:

#### 🐰 **RabbitMQ — для асинхронных событий (Event-driven)**
**Когда используем:** "Fire and forget" — отправил событие и не жду ответа
```python
# ✅ Примеры правильного использования RabbitMQ:
await rabbitmq.publish("user.registered", UserRegisteredEvent(user_id=123))
await rabbitmq.publish("vacancy.found", VacancyFoundEvent(vacancy_id=456))
await rabbitmq.publish("application.sent", ApplicationSentEvent(user_id=123, vacancy_id=456))

# Преимущества:
# - Слабое связывание (сервисы не знают друг о друге)
# - Высокая производительность (не блокирует отправителя)
# - Отказоустойчивость (очереди переживают падения сервисов)
```

#### 🌐 **FastAPI HTTP — для синхронных запросов (Request-Response)**
**Когда используем:** нужен **немедленный ответ** с данными для продолжения работы
```python
# ✅ Примеры правильного использования HTTP API:
user_data = await http_client.get(f"http://user-service/users/{user_id}")
vacancies = await http_client.get(f"http://vacancy-service/search?query=python")
is_applied = await http_client.get(f"http://application-service/check/{vacancy_id}/{user_id}")

# Преимущества:
# - Немедленный ответ (синхронность)
# - Простота отладки (стандартный HTTP)
# - Естественная семантика запрос-ответ
```

#### ❌ **Типичные ошибки при выборе протокола:**
```python
# ❌ ПЛОХО: использовать RabbitMQ когда нужен ответ
@bot.message_handler(commands=['profile'])
async def show_profile(message):
    await rabbitmq.publish("get_user_data", {"user_id": 123})
    # Как получить ответ? Сложно и медленно!

# ✅ ХОРОШО: HTTP для получения данных
@bot.message_handler(commands=['profile'])
async def show_profile(message):
    user_data = await user_service.get_user(123)  # Получили данные сразу
    await bot.send_message(chat_id, f"Профиль: {user_data.name}")
```

#### 🎯 **Практическое правило выбора:**
- **События** (что-то произошло в системе) → **RabbitMQ**
- **Запросы** (нужны данные для UI/логики) → **FastAPI HTTP**

#### 📊 **Конкретные примеры из проекта:**

**RabbitMQ события:**
- `user.registered` — пользователь зарегистрировался → отправить welcome
- `vacancy.found` — найдена подходящая вакансия → уведомить пользователя
- `application.sent` — отклик отправлен → обновить статистику
- `settings.updated` — настройки изменены → пересчитать рекомендации

**HTTP API запросы:**
- `GET /users/{id}` — данные пользователя для показа в профиле
- `GET /vacancies/search` — список вакансий для отображения
- `POST /applications/apply` — отправить отклик (нужен результат)
- `GET /applications/status/{id}` — проверить статус отклика

### Clean Architecture внутри сервисов
Каждый микросервис структурирован по принципам Clean Architecture:

- **Domain (Доменный слой):** бизнес-логика, модели, интерфейсы
- **Application (Сервисный слой):** координация сценариев, сервисы, use-case'ы
- **Infrastructure (Инфраструктурный слой):** работа с внешними API (hh.ru), БД, Telegram API
- **Presentation (Внешний слой):** Telegram-бот, обработчики команд, UI-сервисы

Каждый слой зависит только от слоев "внутрь", что позволяет легко менять инфраструктуру, не затрагивая бизнес-логику.

---

## 📂 Структура проекта

```
src/
├── user-service/
│   ├── .venv/                # Изолированное Python окружение
│   ├── pyproject.toml        # Зависимости и настройки проекта
│   ├── alembic/              # Миграции БД для user-service
│   │   ├── versions/
│   │   └── alembic.ini
│   ├── domain/
│   │   ├── models.py        # User, Profile, Settings
│   │   └── interfaces.py    # UserRepository, AuthService
│   ├── application/
│   │   ├── use_cases.py     # RegisterUser, UpdateProfile, ManageSettings
│   │   └── services.py      # UserService, AuthService
│   ├── infrastructure/
│   │   ├── repositories.py  # UserRepositoryImpl
│   │   ├── auth_provider.py # OAuth, JWT handling
│   │   └── rabbitmq.py      # RabbitMQ producer/consumer
│   ├── api/
│   │   ├── routes.py        # FastAPI routes
│   │   └── schemas.py       # Pydantic models for API
│   └── main.py              # Service entry point
│
├── vacancy-service/
│   ├── .venv/                # Изолированное Python окружение
│   ├── pyproject.toml        # Зависимости и настройки проекта
│   ├── alembic/              # Миграции БД для vacancy-service
│   ├── domain/
│   │   ├── models.py        # Vacancy, Filter, SearchCriteria
│   │   └── interfaces.py    # VacancyRepository, SearchService
│   ├── application/
│   │   ├── use_cases.py     # SearchVacancies, FilterVacancies
│   │   └── services.py      # VacancyService, FilterService
│   ├── infrastructure/
│   │   ├── repositories.py  # VacancyRepositoryImpl
│   │   ├── hh_api.py        # HH.ru API client
│   │   └── rabbitmq.py      # RabbitMQ producer/consumer
│   ├── api/
│   │   ├── routes.py        # FastAPI routes
│   │   └── schemas.py       # Pydantic models for API
│   └── main.py              # Service entry point
│
├── application-service/
│   ├── .venv/                # Изолированное Python окружение
│   ├── pyproject.toml        # Зависимости и настройки проекта
│   ├── alembic/              # Миграции БД для application-service
│   ├── domain/
│   │   ├── models.py        # Application, Resume, Response
│   │   └── interfaces.py    # ApplicationRepository, ResumeService
│   ├── application/
│   │   ├── use_cases.py     # ApplyToVacancy, TrackApplications
│   │   └── services.py      # ApplicationService, ResumeService
│   ├── infrastructure/
│   │   ├── repositories.py  # ApplicationRepositoryImpl
│   │   ├── hh_apply_api.py  # HH.ru apply logic
│   │   └── rabbitmq.py      # RabbitMQ producer/consumer
│   ├── api/
│   │   ├── routes.py        # FastAPI routes
│   │   └── schemas.py       # Pydantic models for API
│   └── main.py              # Service entry point
│
├── notification-service/
│   ├── .venv/                # Изолированное Python окружение
│   ├── pyproject.toml        # Зависимости и настройки проекта
│   ├── alembic/              # Миграции БД для notification-service
│   ├── domain/
│   │   ├── models.py        # Notification, Report, Analytics
│   │   └── interfaces.py    # NotificationRepository, ReportService
│   ├── application/
│   │   ├── use_cases.py     # SendNotification, GenerateReport
│   │   └── services.py      # NotificationService, AnalyticsService
│   ├── infrastructure/
│   │   ├── repositories.py  # NotificationRepositoryImpl
│   │   └── rabbitmq.py      # RabbitMQ producer/consumer
│   ├── api/
│   │   ├── routes.py        # FastAPI routes (если нужны)
│   │   └── schemas.py       # Pydantic models for API
│   └── main.py              # Service entry point
│
├── telegram-gateway/
│   ├── .venv/                # Изолированное Python окружение
│   ├── pyproject.toml        # Зависимости и настройки проекта
│   ├── domain/
│   │   ├── models.py        # TelegramUser, Command, CallbackQuery
│   │   └── interfaces.py    # BotService, UIService
│   ├── application/
│   │   ├── handlers/        # Command handlers by domain
│   │   │   ├── user_handlers.py
│   │   │   ├── vacancy_handlers.py
│   │   │   └── application_handlers.py
│   │   ├── services/
│   │   │   └── ui_service.py # Telegram UI (keyboards, messages)
│   │   └── middleware.py    # Auth, logging, rate limiting
│   ├── infrastructure/
│   │   ├── telegram_bot.py  # Bot initialization and routing
│   │   ├── service_clients/ # HTTP clients for other services
│   │   └── rabbitmq.py      # RabbitMQ producer/consumer
│   └── main.py              # Service entry point
│
├── shared/
│   ├── events/              # Domain events and event bus
│   ├── exceptions/          # Common exceptions
│   └── utils/               # Common utilities
│
├── docker-compose.yml       # Все сервисы + RabbitMQ + PostgreSQL
├── config.py                # Global configuration
└── main.py                  # Application orchestrator
```

---

## � Независимость микросервисов

### Ключевые принципы независимости

**Каждый микросервис полностью автономен:**

1. **Собственное окружение Python** (`.venv`) с изолированными зависимостями
2. **Отдельный `pyproject.toml`** с уникальными зависимостями для каждого сервиса
3. **Собственная база данных** и миграции (Alembic)
4. **Независимый деплой** — можно обновлять сервисы по отдельности
5. **Собственный жизненный цикл** — разные версии, релизы, роллбеки

### Технический стек для коммуникации

- **RabbitMQ** — асинхронная передача событий между сервисами
- **FastAPI** — HTTP API для синхронных запросов
- **PostgreSQL** — отдельная схема БД для каждого сервиса
- **Docker** — контейнеризация и оркестрация сервисов

### Примеры событий через RabbitMQ

```python
# user-service отправляет событие
await rabbitmq_publisher.publish(
    exchange="user.events",
    routing_key="user.registered",
    message=UserRegisteredEvent(user_id=123, telegram_id=456)
)

# notification-service получает событие
@rabbitmq_consumer.subscribe("user.registered")
async def handle_user_registered(event: UserRegisteredEvent):
    await send_welcome_notification(event.user_id)
```

### Примеры HTTP API между сервисами

```python
# telegram-gateway делает запрос к user-service
class UserServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def get_user(self, user_id: int) -> User:
        response = await self.client.get(f"{self.base_url}/users/{user_id}")
        return User.parse_obj(response.json())
    
    async def update_settings(self, user_id: int, settings: dict) -> bool:
        response = await self.client.put(
            f"{self.base_url}/users/{user_id}/settings", 
            json=settings
        )
        return response.status_code == 200

# Использование в telegram-gateway
@dp.message_handler(commands=['profile'])
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    
    # Синхронный запрос - получаем данные немедленно
    user = await user_service_client.get_user(user_id)
    await message.reply(f"Профиль: {user.name}, статус: {user.status}")
    
    # Асинхронное событие - уведомляем о просмотре профиля
    await rabbitmq.publish("user.profile_viewed", {
        "user_id": user_id,
        "timestamp": datetime.now()
    })
```

### Performance & Reliability considerations

**RabbitMQ:**
- ⚡ **Производительность:** ~50k+ сообщений/сек
- 🛡️ **Надежность:** персистентные очереди, подтверждения доставки
- 📈 **Масштабирование:** кластеризация, шардинг

**HTTP API:**
- ⚡ **Производительность:** ~1k-10k запросов/сек (зависит от логики)
- 🛡️ **Надежность:** retry policies, circuit breakers
- 📈 **Масштабирование:** load balancing, connection pooling

```python
# Пример обработки ошибок для HTTP
async def get_user_with_retry(user_id: int, max_retries: int = 3) -> User:
    for attempt in range(max_retries):
        try:
            return await user_service_client.get_user(user_id)
        except httpx.RequestError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Преимущества такой архитектуры

- **Масштабируемость** — каждый сервис можно масштабировать независимо
- **Надежность** — падение одного сервиса не ломает всю систему
- **Технологическое разнообразие** — можно использовать разные технологии в сервисах
- **Командная работа** — разные команды могут работать над разными сервисами
- **Быстрые релизы** — можно деплоить изменения в одном сервисе без остановки других

---

## �🔗 Взаимосвязь слоев

- **Handlers** (presentation) принимают команды пользователя и вызывают **use-case'ы** (application).
- **Use-case** реализует сценарий (например, "откликнуться на все вакансии по фильтру"), используя сервисы и репозитории из **domain** и **infrastructure**.
- **UIService** строит сообщения и клавиатуры для Telegram, не зная о деталях бизнес-логики.
- **Infrastructure** реализует работу с внешними сервисами (hh.ru, БД, Telegram API) через интерфейсы из **domain**.

---

## 🧩 Принципы и лучшие практики

- **SRP (Single Responsibility Principle):** Каждый модуль отвечает только за одну задачу.
- **Инверсия зависимостей:** Вся бизнес-логика зависит только от абстракций, а не от конкретных реализаций.
- **Тестируемость:** Легко писать unit-тесты для бизнес-логики, мокая инфраструктуру.
- **Масштабируемость:** Можно легко добавить новые сценарии (например, автозаполнение резюме, рассылка уведомлений).
- **Изоляция UI:** Весь Telegram UI (тексты, клавиатуры) вынесен в отдельный сервис.

---

## 🚀 Пример сценария "Автоотклик"

1. **Пользователь** выбирает фильтр вакансий через Telegram-бота.
2. **Handler** вызывает use-case "Автоотклик".
3. **Use-case**:
    - Получает список вакансий через hh_api.
    - Фильтрует их по заданным критериям.
    - Для каждой вакансии вызывает метод отклика через hh_api.
    - Сохраняет результаты в репозиторий.
4. **UIService** формирует отчет и отправляет пользователю.

---

## 🛠️ Как начать новый проект

1. **Скопируйте структуру папок и файлов.**
2. **Определите доменные модели** (User, Vacancy, Resume, Application).
3. **Опишите интерфейсы репозиториев и сервисов** в domain/interfaces.py.
4. **Реализуйте инфраструктурные классы** (работа с hh.ru, БД, Telegram).
5. **Опишите use-case'ы** в application/use_cases.py.
6. **Создайте UIService** для построения сообщений и клавиатур.
7. **Опишите обработчики команд** в application/handlers.py.
8. **Запустите main.py** — и ваш бот готов!

---

## 📚 Пример кода UIService

```python
class BotUIService:
    def __init__(self, ...):
        # сервисы форматирования, прав, пагинации и т.д.
        ...

    def build_main_menu(self, user: User) -> dict:
        # Возвращает клавиатуру главного меню
        ...

    def build_vacancy_list(self, vacancies: list[Vacancy], page: int) -> dict:
        # Клавиатура для просмотра вакансий с пагинацией
        ...
```

---

## � Рабочий процесс и Git workflow

### Правила именования веток

Используется следующая структура для именования веток:
```
<тип>/<сервис>/<описание>
```

**Типы веток:**
- `feature/` — новая функциональность
- `fix/` — исправление багов
- `refactor/` — рефакторинг без изменения функциональности
- `docs/` — изменения в документации

**Названия сервисов:**
- `user-service` — изменения в сервисе пользователей
- `vacancy-service` — изменения в сервисе вакансий
- `application-service` — изменения в сервисе откликов
- `notification-service` — изменения в сервисе уведомлений
- `telegram-gateway` — изменения в Telegram gateway
- `shared` — изменения в общих компонентах

**Примеры веток:**
```
feature/user-service/oauth-integration
fix/vacancy-service/search-filters
refactor/telegram-gateway/message-handlers
docs/application-service/api-documentation
```

### Процесс разработки

1. **Создание ветки** от `dev` с правильным именованием
2. **Разработка** функциональности в отдельной ветке
3. **Создание Pull Request** в ветку `dev`
4. **Code Review** от [@KonakovI](https://github.com/KonakovI)
5. **Слияние в dev** после одобрения (approval)
6. **Деплой** в production из ветки `dev`

### Пошаговые команды для работы с ветками

#### 1. Начало работы (создание новой ветки)
```bash
# Переключиться на dev и обновить до последней версии
git switch dev
git pull origin dev

# Создать новую ветку от актуального dev
git switch -c feature/user-service/oauth-integration
```

#### 2. Процесс разработки
```bash
# Внести изменения в код...

# Добавить все изменения в staging
git add .

# Создать коммит с правильным сообщением
git commit -m "feature: добавлена авторизация через hh.ru OAuth"

# При первом push новой ветки
git push --set-upstream origin feature/user-service/oauth-integration

# При последующих push (после установки upstream)
git push
```

#### 3. Обновление ветки во время разработки
```bash
# Если dev обновился во время вашей работы
git switch dev
git pull origin dev
git switch feature/user-service/oauth-integration
git rebase dev  # или git merge dev
```

#### 4. Завершение работы
```bash
# Убедиться, что все изменения запушены
git push

# Создать Pull Request через GitHub/GitLab UI
# После одобрения и слияния удалить локальную ветку
git switch dev
git pull origin dev
git branch -d feature/user-service/oauth-integration
```

#### 🔥 Важные правила:
- **Всегда** начинать от актуального `dev`
- **Никогда** не пушить напрямую в `dev` или `main`
- **Обязательно** использовать правильные названия веток и коммитов
- **Регулярно** синхронизироваться с `dev` во время долгой разработки

### Правила именования коммитов

Используется следующий формат для сообщений коммитов:
```
<тип>: краткое описание на русском языке
```

**Типы коммитов:**
- `feature:` — новая функциональность
- `fix:` — исправление багов
- `update:` — обновление существующей функциональности
- `refactor:` — рефакторинг кода без изменения функциональности
- `docs:` — изменения в документации
- `test:` — добавление или изменение тестов
- `config:` — изменения в конфигурации

**Примеры коммитов:**
```
feature: добавлена авторизация через hh.ru OAuth
fix: исправлена ошибка при поиске вакансий
update: улучшен алгоритм фильтрации вакансий
refactor: выделен общий HTTP клиент в отдельный класс
docs: обновлена документация API user-service
test: добавлены тесты для vacancy-service
config: настроен docker-compose для разработки
```

**Рекомендации:**
- Описание должно быть кратким (до 50 символов)
- Использовать повелительное наклонение ("добавлена", а не "добавляю")
- Не использовать точку в конце
- Описание должно отвечать на вопрос "что сделано?"

### Основные ветки
- `main` — production-ready код
- `dev` — интеграционная ветка для разработки
- `feature/*` — разработка новых функций

---

## �📦 Пример зависимостей

- aiogram / pyTelegramBotAPI — Telegram Bot API
- httpx / requests — для работы с hh.ru API
- SQLAlchemy / asyncpg — для работы с БД
- pydantic — для моделей и валидации

---

## 🏛️ Архитектурные решения и обоснования

### Почему именно RabbitMQ + FastAPI?

**Альтернативы, которые мы отвергли:**
1. **Только HTTP** — блокирует отправителя, создает сильную связанность
2. **Только Message Queue** — сложно получать данные, требует дополнительную логику для запрос-ответ
3. **gRPC** — избыточная сложность для наших задач, проблемы с debugging
4. **WebSockets** — не подходит для межсервисного взаимодействия

**Наше решение — гибридный подход:**
```python
# Событийно-ориентированная архитектура для бизнес-событий
if event_type == "business_event":  # user_registered, vacancy_found
    use_rabbitmq()

# Request-Response для получения данных
if need_immediate_response:  # get_user, search_vacancies  
    use_http_api()
```

### Технические детали

**RabbitMQ Exchange Types в проекте:**
- **Topic Exchange** — для событий (`user.registered`, `vacancy.found`)
- **Direct Exchange** — для команд (`send.notification`, `process.application`)

**HTTP API Design Patterns:**
- **RESTful** — стандартные CRUD операции
- **Circuit Breaker** — защита от каскадных падений
- **Retry with Exponential Backoff** — устойчивость к временным сбоям

### Мониторинг и отладка

```python
# Логирование для RabbitMQ событий
logger.info(f"Event published: {event_type}", extra={
    "event_id": event.id,
    "routing_key": routing_key,
    "timestamp": datetime.now()
})

# Метрики для HTTP API
@metrics.timer("user_service.get_user.duration")
async def get_user(user_id: int):
    # ... implementation
```

---

## 📝 Итог

**Эта структура позволяет быстро и удобно разрабатывать сложные Telegram-боты для автоматизации любых задач, в том числе работы с hh.ru API.**

---

> **Совет:**  
> Всегда начинайте с описания бизнес-логики и интерфейсов, а инфраструктуру реализуйте последней.  
> UI держите максимально изолированным — это упростит поддержку и масштабирование.



```
/Users/aleksejzadoroznyj/PycharmProjects/hhtgbot/hh_auto_response/src/user-service/.venv/bin/python
```
