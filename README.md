# Barter Project

## Описание проекта

Barter Project — это платформа для обмена вещами (бартер), которая позволяет пользователям создавать объявления, искать предложения для обмена и взаимодействовать через удобный REST API.  
Проект реализован на Django с использованием Django REST Framework и PostgreSQL, с контейнеризацией через Docker.

В проекте предусмотрена документация API с помощью Swagger (drf-spectacular), что облегчает интеграцию и тестирование.

---

## Стек технологий

- Python 3.10+  
- Django 5.2  
- Django REST Framework  
- PostgreSQL  
- Docker & Docker Compose  
- drf-spectacular (Swagger/OpenAPI)  
- Gunicorn  
- Pre-commit (black, flake8, isort)  

---

## Инструкция по запуску

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Nurba-Developer/barter_project.git
cd barter_project
````

### 2. Создать `.env` файл

Скопируйте пример и заполните своими значениями:

```bash
cp .env.example .env
```

### 3. Запустить проект через Docker

```bash
docker-compose up --build
```

### 4. Применить миграции и создать суперпользователя

В отдельном терминале:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. Открыть проект в браузере

* API доступен по адресу: [http://localhost:8000/](http://localhost:8000/)
* Документация OpenAPI (Swagger UI): [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
* OpenAPI схема JSON: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

---

## Примеры API

### Получить список объявлений

```http
GET /api/ads/
```

Ответ:

```json
[
  {
    "id": 1,
    "title": "Объявление 1",
    "category": "electronics",
    "condition": "new",
    "description": "Описание объявления",
    "created_at": "2025-07-15T10:00:00Z"
  },
  ...
]
```

### Создать объявление

```http
POST /api/ads/
Content-Type: application/json

{
  "title": "Новая вещь",
  "category": "furniture",
  "condition": "used",
  "description": "Отдам в хорошие руки"
}
```

## Документация API

Проект использует [drf-spectacular](https://drf-spectacular.readthedocs.io/) для генерации OpenAPI схемы и Swagger UI.

* OpenAPI схема доступна по пути: `/api/schema/`
* Swagger UI — интерактивная документация: `/api/docs/`
