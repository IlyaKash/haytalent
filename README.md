### Запуск в Docker

Создать файл .env в корне проекта и скопировать туда данные из .enx.exemple

Приложение, база данных и тесты запускаются через docker-compose:

```docker-compose up -d```

Проверить запуск контейнеров:

```docker ps`

Что произойдёт:
Поднимется база данных db
Применятся миграции Alembic
Запустится сервис api на порту 8000
Отдельный контейнер tests выполнит pytest

Доступ к приложению: [http://localhost:8000](http://localhost:8000)
Документация OpenAPI [http://localhost:8000/docs](http://localhost:8000/docs)