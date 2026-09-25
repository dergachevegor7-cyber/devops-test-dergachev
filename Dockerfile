FROM python:3.12-slim

WORKDIR /code

# Зависимости ставятся отдельным слоем: пока requirements.txt не меняется,
# Docker берёт этот слой из кэша и не переустанавливает пакеты при правках кода.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
