# Используем официальный образ Python в качестве базового образа
FROM python:3.12-slim
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Копируем файл requirements.txt внутрь контейнера
COPY requirements.txt ./
COPY . .
# Устанавливаем зависимости, описанные в файле requirements.txt
# install python dependencies
COPY requirements.txt /app/requirements.txt
#RUN python -m venv venv
RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install --no-cache-dir -r requirements.txt
# running migrations
CMD ["python", "manage.py", "migrate"
#CMD ["python", "manage.py", "collectstatic", "--noiput"]
# gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "django_girls.wsgi"]
#CMD ["python", "manage.py", "collectstatic"]
EXPOSE 8000
