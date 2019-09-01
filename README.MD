# Old school IM
Проект написаный в качестве выполнения тестового задания.

## Требования
* PostgreSQL 9.4 или выше
* psycopg2 (`pip3 install psycopg2`)

## Запуск
1. Создайте на сервере базу данных с именем *old_school_im*.

2. В файле *old_school_im/settings.py* в словаре `DATABASES` настройте подключение к серверу баз данных.

   Текущая настройка: `localhost:5432`, логин `postgres`, пароль пустой.

3. Запустите команду `python3 manage.py migrate` из корня проекта.

4. Запустите команду `python3 manage.py createsuperuser`

5. Запустите сервер `python3 manage.py runserver`

6. Создайте несколько пользователей на странице http://127.0.0.1:8000/admin/auth/user/

7. Добавте их к себе в контакты на странице http://127.0.0.1:8000/im/chats

