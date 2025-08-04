Для данного приложения использовался Python 3.11.6 + библиотеки FastAPI, pydantic, sqlite3, csv, selenium и т.д. (полный
список в файле requirements.txt)

Для запуска приложения с помощью CLI-интерфейс необходимо, находясь в корневой директории проекта, запустить команды для
создания базы данных или файла формата CSV соответственно:
python main.py --max 50 --output databaseDB.db --db
python main.py --max 50 --output fileCSV.csv

Команды вызывающие справку с инструкцией CLI-интерфейса:
python main.py --help
python main.py -h

Приложение загрузки тендеров с сайта https://www.b2b-center.ru/market/

options:
-h, --help show this help message and exit
--max MAX Число тендеров для загрузки.
--output OUTPUT Название и формат файла для сохранения результатов.
--db Флаг БД. При его наличии создается файл формата .db

Пример использования: python main.py --max 20 --output databaseDB.db --db

Для запуска роутера FastAPI необходимо запустить файл "main_fastapi_v1.py", перейти по адресу http://127.0.0.1:8000 (
Эндпоинт реализовался под документацию Swagger: http://127.0.0.1:8000/docs)