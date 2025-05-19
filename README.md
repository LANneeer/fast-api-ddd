# 💸 Currency Transfer Service

REST API для мультивалютных переводов между счетами. Поддерживает регистрацию пользователей, создание аккаунтов, переводы с учётом комиссий и конвертации валют.

---

## 📦 Технологии

- **DDD-архитектура**
- **Python 3.10+**
- **FastAPI** — REST API
- **SQLAlchemy (async)** — ORM
- **Alembic** — миграции БД
- **Pydantic** — DTO и валидация
- **JWT** — аутентификация
- **PostgreSQL** / SQLite

---

## ⚙️ Установка

```bash
git clone https://github.com/yourname/currency-transfer-service.git
cd currency-transfer-service

python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🗃️ Миграции

```bash
alembic upgrade head
```

---

## 🚀 Запуск

```bash
uvicorn app.main:app --reload
```

Открой Swagger UI:
```
http://localhost:8000/docs
```

---

## 🔐 Аутентификация

Используется JWT:

1. `POST /auth/login` — логин с email и паролем
2. Скопируй `access_token`
3. Нажми "Authorize" в Swagger UI и вставь:
   ```
   Bearer <your_token>
   ```

---

## 🧭 API Эндпоинты

### 👤 Пользователи
- `POST /users/` — регистрация
- `GET /users/me` — текущий пользователь

### 🔑 Авторизация
- `POST /auth/login` — вход по email и паролю

### 💳 Аккаунты
- `POST /accounts/` — создать счёт
- `GET /accounts/` — список счетов пользователя
- `GET /accounts/{id}` — получить счёт
- `PUT /accounts/{id}` — изменить валюту
- `DELETE /accounts/{id}` — удалить счёт

### 💸 Переводы *(скоро)*
- `POST /transfers/` — перевод с комиссией и конвертацией
- `GET /transfers/` — история операций

---

## 🧱 Структура проекта (DDD)

```
./
├── alembic/ # Миграции базы данных (Alembic)
├── app/
│ ├── contrib/ # Общие зависимости (если есть)
│ ├── core/ # Конфигурации и общие файлы
│ ├── domains/ # Бизнес-логика (DDD)
│ │ ├── accounts/
│ │ │ ├── abstration.py # Абстракция (репозиторий/сервис)
│ │ │ ├── model.py # Доменная модель Account
│ │ │ └── service.py # Логика аккаунтов
│ │ └── users/
│ │ ├── abstraction.py # Абстракция (репозиторий/сервис)
│ │ ├── model.py # Доменная модель User
│ │ └── service.py # Логика пользователей
│ ├── dto/
│ │ ├── accounts.py # DTO для Account
│ │ ├── auth.py # DTO для Login / Token
│ │ └── users.py # DTO для User
│ ├── gateway/
│ │ └── routers/ # FastAPI маршруты
│ │ ├── accounts.py # /accounts endpoints
│ │ ├── auth.py # /auth endpoints
│ │ └── users.py # /users endpoints
│ ├── infrastructure/
│ │ ├── accounts/
│ │ │ └── orm.py # ORM-модель Account
│ │ └── users/
│ │ ├── orm.py # ORM-модель User
│ │ └── dependencies.py # Depends: get_current_user и т.д.
│ ├── repository/
│ │ ├── accounts.py # Реализация AccountRepository
│ │ └── users.py # Реализация UserRepository
│ ├── utils/
│ │ ├── config.py # Настройки БД и окружения
│ │ └── init.py
│ └── main.py # Точка входа FastAPI
├── tests/ # Тесты (в разработке)
├── README.md # Документация проекта
├── alembic.ini # Настройки Alembic
├── dev.db # SQLite база (для dev)
└── requirements.txt # Зависимости проекта
```

---

## 🧪 Тесты (в будущем)

```bash
pytest -v
```

---

