# Кабинет сотрудника (MVP)

Внутренний портал для сотрудников: вход с двухфакторной аутентификацией (TOTP),
личный кабинет и заявки на справки. Для HR-системы предусмотрен REST API
(создание сотрудников, просмотр и обработка заявок).

## Стек

- Python 3.14, Django 6.1, Django REST Framework 3.18
- PyOTP — одноразовые коды TOTP (Google Authenticator и совместимые)
- SQLite, аутентификация DRF по токенам (`rest_framework.authtoken`)

## Быстрый старт

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # доступ к админке
python manage.py runserver
```

- Админка: http://127.0.0.1:8000/admin/
- Вход в кабинет: http://127.0.0.1:8000/login/

### Токен для API

```bash
python manage.py drf_create_token <username>
```

Токен передаётся в заголовке: `Authorization: Token <token>`.

## Как это работает

1. Сотрудник создаётся через API (или админку). В ответе возвращаются
   `username`, временный `password` и `totp_secret` — секрет для добавления
   аккаунта в приложение-аутентификатор.
2. При входе сотрудник вводит логин и пароль. Если у пользователя задан
   `totp_secret`, запрашивается одноразовый код (`/totp/`).
3. После успешного входа — дашборд. Выход — кнопка на дашборде (POST-форма).

## Веб-интерфейс

| URL      | Описание                                            |
|----------|-----------------------------------------------------|
| `/login/`  | Вход (логин + пароль)                              |
| `/totp/`   | Ввод одноразового кода (если включён TOTP)         |
| `/`        | Дашборд (только для авторизованных)                |
| `/logout`  | Выход (только POST)                                |
| `/admin/`  | Админка: пользователи и заявки на справки          |

## API

| Метод | URL                         | Auth   | Описание |
|-------|-----------------------------|--------|----------|
| GET   | `/api/ping/`                | нет    | Проверка живости |
| POST  | `/api/employees/`           | Token  | Создание сотрудника |
| GET   | `/api/certificates/`        | Token  | Список всех заявок на справки |
| GET   | `/api/certificates/<id>/`   | Token  | Карточка заявки |
| PATCH | `/api/certificates/<id>/`   | Token  | Смена `status`, `admin_comment` |

### Примеры

Создание сотрудника:

```http
POST /api/employees/
Authorization: Token <token>
Content-Type: application/json

{"uuid": "5f0d9d5e-2a4c-4a7e-9a2b-1c3d5e7f9a1b", "username": "ivanov"}
```

Ответ `201`:

```json
{
  "uuid": "5f0d9d5e-2a4c-4a7e-9a2b-1c3d5e7f9a1b",
  "username": "ivanov",
  "totp_secret": "JBSWY3DPEHPK3PXP",
  "password": "pQ9_x2Lm-N4"
}
```

Смена статуса заявки:

```http
PATCH /api/certificates/1/
Authorization: Token <token>
Content-Type: application/json

{"status": "ready", "admin_comment": "Готово, можно забрать"}
```

## Модель данных

**User** (`cabinet.User`, наследует `AbstractUser`):
- `uuid` — внешний идентификатор сотрудника (заполняется через API)
- `totp_secret` — секрет TOTP; пустой = 2FA отключена для пользователя

**CertificateRequest** — заявка на справку:
- `user` — сотрудник
- `certificate_type` — `income` (о доходах), `employment` (с места работы),
  `vacation` (об отпусках), `other` (прочее)
- `description` — комментарий сотрудника (период, цель)
- `status` — `created` → `processing` → `ready` / `rejected`
- `admin_comment` — комментарий ответственного
- `created_at`, `updated_at`

Подача заявок пока — через админку; REST API заявок рассчитан на сервисный
токен HR-системы (возвращает заявки всех сотрудников).

## Структура проекта

```
config/    настройки и URL-конфигурация проекта
cabinet/   пользователи, веб-кабинет (login/totp/dashboard/logout), модели заявок
api/       REST API (DRF): сотрудники, заявки
```

## Известные ограничения MVP

- `password` и `totp_secret` возвращаются в открытом виде — деплой только по HTTPS.
- Нет ограничения числа попыток ввода TOTP-кода.
- В форме входа не выводится сообщение о неверном логине/пароле.
- API заявок не фильтруется по пользователю (рассчитан на сервисный токен).
- `DEBUG = True`, `SECRET_KEY` в настройках — перед продом вынести в переменные окружения.
- SQLite и консольный email-backend — заменить при переходе в продакшен.
- Тестов пока нет.

## Roadmap

- Форма подачи заявки на справку в кабинете + список своих заявок со статусами.
- Ограничение попыток TOTP.
- Сообщения об ошибках в форме входа.
- Разделение API на «сотрудник» и «сервис» (фильтрация по `request.user`).
- Покрытие тестами.
