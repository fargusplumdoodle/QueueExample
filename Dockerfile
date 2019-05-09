# My Site
# Version: 1.0

FROM python:3

# Project Files and Settings
ARG PROJECT=Nettacker
ARG PROJECT_DIR=/var/www/${PROJECT}

RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY . .

RUN pip install -r requirements.txt

# updating database
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# for example: we could put this here to ensure we dont make broken containers
RUN python manage.py test

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
