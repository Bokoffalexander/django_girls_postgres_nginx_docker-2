sudo docker-compose run django python manage.py makemigrations &&
sudo docker-compose run django python manage.py migrate &&
sudo docker-compose run django python manage.py collectstatic --noinput &&
sudo docker-compose up --build
