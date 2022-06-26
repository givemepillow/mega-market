# Второе вступительное задание в ШБР.
REST API сервис, который позволяет магазинам загружать и обновлять информацию о товарах, а пользователям - смотреть какие товары были обновлены за последние сутки, а также следить за динамикой цен товара или категории за указанный интервал времени.

### API сервиса реализует *[спецификацию](docs/openapi.yaml)* в соответствии с *[заданием](docs/Task.md)*.

### Инструкция по запуску приложения
1. Для запуска в **Docker**.

> В папке с файлом `docker-compose.yml` выполнить следующие команды:
> ```shell
> docker-compose build
> docker-compose up
> ```

2. Запуск без **Docker** - вручную.

> Сначала необходимо установить [Poetry](https://python-poetry.org/docs/):
> ```shell
> curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
> ```
>Затем получить `requirements.txt` и выполнить установку пакетов:
> ```shell
> poetry export -f requirements.txt --output requirements.txt --without-hashes
> pip install -r requirements.txt
> ```
> Далее необходимо убедиться, что создана база данных в PostgreSQL,
> и выполнить миграции в папке с приложением, указав значения для вашей БД:
> ```shell
> cd market
> # Пример url: market_app:backend_school_2022@localhost:5432/mega_market
> alembic -x url=<имя_пользователя>:<пароль>@<адрес>:<порт>/<название_вашей_базы_данных> upgrade head
> cd -
> ```
> Поле выполнения миграций остаётся установить переменные окружения:
> ```shell
> export DB_URL=<имя_пользователя>:<пароль>@<адрес>:<порт>/<название_вашей_базы_данных>
> ```
> И запустить приложение:
> ```shell
> uvicorn market.api.main:app --port 80
> ```
