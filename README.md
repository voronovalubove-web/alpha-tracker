# Alpha-Soft Task Tracker API

REST API для управления проектами и задачами. Разработано на Django REST Framework.

## 🛠 Стек
- Python 3.10+, Django 4.2+, DRF 3.14+
- `django-filter` — фильтрация задач
- `drf-spectacular` — авто-документация (Swagger/ReDoc)

## 🚀 Быстрый старт

```bash
# 1. Клонируй и перейди в проект
git clone https://github.com/voronovalubove-web/alpha-tracker.git
cd alpha-tracker

# 2. Создай окружение и установи зависимости
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Примените миграции и создай пользователя
python manage.py migrate
python manage.py createsuperuser

# 4. Запусти сервер
python manage.py runserver
