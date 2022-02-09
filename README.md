# praktikum_new_diplom

## Запуск проекта через Docker

Собрать контейнер:
- docker-compose up -d

Выполнить следующие команды:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate --noinput 
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```
Заполнить бд ингредиентами:
```
docker-compose exec backend python manage.py load_ingredients
```


## Запуск проекта в dev-режиме

- Установить и активировать виртуальное окружение
- Установить зависимости из файла requirements.txt
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```
- Выполнить миграции:
```
python manage.py migrate
```

- В папке с файлом manage.py выполнить команду:
```
python manage.py runserver
```

- Для загрузки ингредиентов:
```
python manage.py load_ingredients
```
