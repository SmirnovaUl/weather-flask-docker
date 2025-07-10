1. Как собрать и запустить проект:

Убедитесь, что установлен и запущен Docker Desktop.

Клонируйте репозиторий и перейдите в папку с проектом:
   cd path/to/your/project/docker

Соберите и запустите все сервисы:
   docker-compose up --build
Это создаст и запустит контейнеры для backend, PostgreSQL и nginx.

Остановить сервисы:
   docker-compose down

2. Как проверить, что проект работает:

Через браузер 

Откройте http://localhost — главная страница приложения.

Проверьте эндпоинты:
http://localhost/ping — должен вернуть "PONG".
http://localhost/health — должен вернуть {"status": "HEALTHY"}.
http://localhost/list — должен показать список городов и температуру.

Через curl

curl http://localhost/ping
curl http://localhost/health
curl http://localhost/list

3. Как проверить подключение к PostgreSQL:

Через psql в контейнере

Выполните команду для входа в psql внутри контейнера:
Apply to app.py

Внутри psql выполните:
Apply to app.py

Через pgAdmin

Подключитесь с параметрами:
Host: localhost
Port: 5432
User: postgres
Password: MJWhzCSaU
Database: weather

Проверьте наличие таблицы weather и её содержимое.
