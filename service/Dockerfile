FROM python:3.9

WORKDIR /src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /src/app/

RUN pip install -r requirements.txt

COPY . /src/app/