FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install Flask

RUN pip install Flask-Cors

RUN pip install Flask-RESTful

RUN pip install Flask-SQLAlchemy

EXPOSE 8080

CMD ["python", "./app.py"]
