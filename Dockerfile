FROM python:3.10-slim

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

# Получаем список зависимотсей с помощью пакетного менеджера poetry и устанавливаем их.
RUN pip install poetry==1.1.13 && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /app

COPY ./market /app/market

EXPOSE 80

