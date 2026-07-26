# 📰 News Aggregator

Новостной агрегатор на Django с автоматическим парсингом RSS-лент.

## 🚀 Функционал

- Парсинг новостей из RSS
- Автоматическое определение категорий
- Фильтрация по категориям
- Адаптивный дизайн с неоновой темой
- Аутентификация пользователей

## 🛠 Стек

- Django 5.0
- PostgreSQL
- Bootstrap 5
- Python 3.13

## 📦 Установка

``bash
git clone https://github.com/yuriy0770/agregator_news.git
cd agregator_news
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


## 📁 **Структура проекта (что залить на GitHub)**
agregator_news/
├── main/
│ ├── management/
│ │ └── commands/
│ │ └── parse_news.py
│ ├── templates/
│ │ └── main/
│ ├── models.py
│ ├── views.py
│ └── urls.py
├── users/
├── config/
├── static/
├── media/
├── .gitignore
├── requirements.txt
├── README.md
├── .env.example
└── manage.py
