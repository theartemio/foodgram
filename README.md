# Foodgram

Перед вами Foodgram - проект для ваших самых смелых кулинарных экспериментов!

Репозиторий представляет собой полностью рабочий бэкенд и фронтенд для кулинарного сайта, а также готовый воркфлоу для CI/CD проекта на сервере в докер-контейнерах.

## Установка и настройка (весь функционал)

1. Клонируйте репозиторий:

```bash
git clone git@github.com:theartemio/foodgram.git
```

2. Разверните проект:

Используйте команду

```bash
docker compose up --build
```

В корневой директории проекта

## Установка и настройка (бэкенд отдельно)

1. Клонируйте репозиторий:

```bash
git clone git@github.com:theartemio/foodgram.git
```

2. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите необходимые зависимости:

```bash
pip install -r requirements.txt
```

4. Выполните миграции:

```bash
python manage.py migrate
```

5. При необходимости загрузите базу данных из .csv файлов с помощью команды:

```bash
python manage.py import_csv
```

## Использование

### Регистрация пользователя через API

POST api/users/ — передайте эмейл, имя, фамилию, юзернейм, и пароль, чтобы зарегистрироваться.
Пример запроса:

```json
{
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "username": "string",
  "password": "string"
}
```

### Аутентификация и получение токена

POST api/auth/token/login/ — передайте юзернейм и полученный код подтверждения, чтобы получить токен.
Пример запроса:

```json
{
    "email": "user@example.com",
    "password": "string"
}
```


## Требования
- Python 3.8+
- Django 3.2+
- Djangorestframework 3.12+

## Авторы

**Бэкенд, Докер, CI/CD**
Артемий Третьяков [GitHub](https://github.com/theartemio)

**Исходный репозиторий**
Яндекс.Практикум [GitHub](https://github.com/yandex-praktikum/).

## Лицензия
Этот проект распространяется на условиях лицензии MIT.
