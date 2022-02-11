![example workflow](https://github.com/Igoryarets/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Проект продуктовый помощник Foodgram

## Проект доступен по адресу 
http://84.201.179.16

Админ: Iyarets (http://84.201.179.16/admin/)
Пароль: 1234@1234
Почта: igoryarets338@gmail.com

Пользователь: vasily@gmail.com
Пароль: 12345@12345

Пользователь: petr@gmail.com
Пароль: 123456@123456

Документация: http://84.201.179.16/api/docs/


## Описание:
```
«Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять 
чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» 
позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 
```

## Запуск с использованием CI/CD

Установить docker, docker-compose на боевом сервере

```
ssh <username>@<server_ip>
sudo apt install docker.io
https://docs.docker.com/compose/install/ # docker-compose
```

Скопируйте файлы docker-compose.yml и nginx/default.conf из директории infra проекта на сервер 
в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.


Заполнить в настройках репозитория секреты:

```
DOCKER_USERNAME  <ваш docker id>

DOCKER_PASSWORD  <ваш docker пароль>

PROJECT_NAME     <ваше имя проекта>

HOST             <ip боевого сервера>

USER             <имя пользователя под которым выполняется вход на сервер>

SSH_KEY          <SSH ключ>

PASSPHRASE       <Если ваш ssh-ключ защищён фразой-паролем>

TELEGRAM_TO      <id telegram аккаунта>

TELEGRAM_TOKEN   <токен вашего бота>

DB_ENGINE        <например: django.db.backends.postgresql>

DB_NAME          <например: postgres>

POSTGRES_USER    <например: postgres>

POSTGRES_PASSWORD <ваш пароль БД>

DB_HOST          <например: db>

DB_PORT          <порт подключения к БД 5432>

```

Запушить проект на гитхаб, затем после успешного workflow на
сервере выполнить:

```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Заполнить бд ингредиентами:
```
sudo docker-compose exec backend python manage.py load_ingredients
```


## Запуск проекта через Docker

Перейти в директорию infra

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


## Запуск проекта в dev-режиме (применимо для backend приложения)

Заменить в settings.py БД. Вместо PostgresSQL 
(можно закомментировать) использовать: 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```

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

- Запустить dev сервер:
```
python manage.py runserver
```

- Для загрузки ингредиентов:
```
В приложении recipce_api  management/commands/load_ingredients.py в
current_dir = r'/data/ingredients.csv' применить current_dir = r'\data\ingredients.csv'

python manage.py load_ingredients
```
