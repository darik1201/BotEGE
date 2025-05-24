FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости первыми для кеширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app

# Добавляем путь для импортов
ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["python", "src/main.py"]