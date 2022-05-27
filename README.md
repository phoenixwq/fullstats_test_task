Для запуска проекта необходимо создать файл .env
со следующим содержимым
```
POSTGRES_DB=DB_NAME
POSTGRES_USER=DB_USERNAME
POSTGRES_PASSWORD=DB_PASSWORD
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
DEBUG=0
SECRET_KEY=foo
DATABASE_URL=postgres://postgres:postgres@db:5432/DB_NAME
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```
Собрать и запустить контейнеры:
```
sudo docker-compose build
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose exec web python manage.py makemigrations --noinput
sudo docker-compose up
```
