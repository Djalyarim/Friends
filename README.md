
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

<h1>Социальная сеть Friends</h1>
Проект развернут на python-anywhere: <h3>https://djalyarim.pythonanywhere.com</h3>

<h2>Friends - это социальная сеть для публикации постов, в которой можно:</h2>

<li>регистрироваться и логиниться, восстанавливать пароль по почте</li>
<li>создавать, редактировать, удалять свой профиль (аватар, описание)</li>
<li>создавать, редактировать, удалять свои записи</li>
<li>просматривать страницы других пользователей</li>
<li>комментировать записи других авторов</li>
<li>подписываться на авторов, просматривать список подписок и подписчиков</li>
<li>Ставить и убирать лайки на публикации</li>
Модерация записей осуществляется через встроенную панель администратора

<h2>Используемые технологии</h2>
<li>Django 2.2</li>
<li>Python 3.8</li>
<li>SQLite</li>
<li>HTML/CSS</li>
<h2>Установка проекта:</h2>

### Клонируйте данный репозиторий
```git clone https://github.com/Djalyarim/hw05_final```
### Создайте и активируйте виртуальное окружение
```
python -m venv venv<br>
source ./venv/Scripts/activate  #для Windows
source ./venv/bin/activate      #для Linux и macOS
```
### Установите требуемые зависимости
```
pip install -r requirements.txt
```
### Примените миграции
```
python manage.py migrate
```
### Запустите django-сервер
```
python manage.py runserver
```

### Приложение будет доступно по адресу: http://127.0.0.1:8000/


