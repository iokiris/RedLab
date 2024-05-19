FROM python:3.10-slim

WORKDIR /app

# копирование зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# копирование всего кода
COPY . .


# запуск на 8000 порт
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
