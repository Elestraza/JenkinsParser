FROM python:latest

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt FlaskAPI.py Config.py JenkinsParser.py /app/

RUN pip install -r requirements.txt

COPY . /app