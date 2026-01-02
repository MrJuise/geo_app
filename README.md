# Geo Messages API

Backend-приложение на Django + Django REST Framework для работы с географическими точками и сообщениями пользователей на карте.

Проект реализует:
- создание точек на карте
- добавление сообщений к точкам
- поиск точек в заданном радиусе
- получение сообщений пользователей в заданном радиусе

Географические вычисления выполняются вручную (формула Haversine), без GeoDjango/PostGIS.

---

## Технологический стек

- Python 3.x
- Django
- Django REST Framework
- SQLite (по умолчанию, можно заменить на PostgreSQL)
- Token Authentication (DRF)

---

## Установка и запуск

1. Клонировать проект

```bash
git clone <repository_url>
cd geo_app
```

2. Создать виртуальное окружение и установить зависимости

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Применить миграции

```bash
python manage.py migrate
```

4. Создать пользователя

```bash
python manage.py createsuperuser
```
5. Запустить сервер

```bash
python manage.py runserver
```
Сервер будет доступен по адресу:

http://127.0.0.1:8000/

## Аутентификация

Используется Token Authentication.
Получение токена

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "YOUR_USERNAME", "password": "YOUR_PASSWORD"}'
```
Ответ:

```bash
{"token": "YOUR_TOKEN"}
```
Токен используется в заголовке:

```bash
Authorization: Token YOUR_TOKEN
```

## Тестирование

Проект содержит базовые автотесты для проверки ключевого функционала API: создание точки, поиск точек в радиусе и поиск сообщений в радиусе. 
Тесты выполняются на отдельной временной тестовой базе данных и не затрагивают рабочие данные.

```bash
python manage.py test
```
Что проверяется:

POST /api/points/ — авторизованный пользователь может создать точку, owner назначается автоматически.

GET /api/points/search/ — поиск возвращает только точки внутри заданного радиуса.

GET /api/messages/search/ — поиск возвращает только сообщения, привязанные к точкам внутри радиуса.

## API Эндпоинты
Создание точки

POST /api/points/

```bash
curl -X POST http://127.0.0.1:8000/api/points/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 52.36, "longitude": 4.90}'
```

Создание сообщения к точке

POST /api/points/messages/

```bash
curl -X POST http://127.0.0.1:8000/api/points/messages/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"point": 1, "content": "Hello from this place"}'
```

Поиск точек в радиусе

GET /api/points/search/

```bash
curl "http://127.0.0.1:8000/api/points/search/?latitude=52.36&longitude=4.90&radius=5" \
  -H "Authorization: Token YOUR_TOKEN"
```
Поиск сообщений в радиусе

GET /api/messages/search/

```bash
curl "http://127.0.0.1:8000/api/messages/search/?latitude=52.36&longitude=4.90&radius=5" \
  -H "Authorization: Token YOUR_TOKEN"
```
## Географическая логика

Для поиска точек и сообщений используется:

    Предварительный отбор по bounding box

    Точный расчёт расстояния по формуле Haversine

Такой подход:

    не требует PostGIS

    работает с SQLite и PostgreSQL

    легко расширяется до GeoDjango при необходимости

Архитектура

    Models — структура данных

    Serializers — валидация и формат API

    Views — логика обработки запросов

    Гео-вычисления вынесены в отдельные функции

    Все эндпоинты защищены авторизацией

Возможные улучшения

    Подключение GeoDjango + PostGIS

    Добавление расстояния до точки в API-ответ

    Кеширование гео-запросов

    Frontend с картой (Leaflet / Mapbox)