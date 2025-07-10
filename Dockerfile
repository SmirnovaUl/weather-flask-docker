FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY Veb.py .
COPY wait_for_db.py .

# Запускаем с ожиданием БД
CMD ["sh", "-c", "python wait_for_db.py && python Veb.py"]