import os

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Схема товара, которую Pydantic проверяет в теле POST /items.

    Если поле отсутствует или его нельзя привести к нужному типу
    (например, price="abc"), FastAPI сам вернёт 422 с описанием ошибки,
    и код обработчика даже не будет вызван.
    """

    name: str
    price: float


# Хранилище товаров в памяти процесса. Данные живут, пока работает uvicorn,
# и пропадают при перезапуске. Каждый воркер имеет свой отдельный список.
items: list[Item] = []


@app.get("/health")
def health():
    """Проверка, что приложение запущено и отвечает на запросы.

    Ничего не проверяет внутри (БД, диски и т.п.), поэтому подходит
    для liveness-проверок балансировщика или мониторинга.
    """
    return {"status": "ok"}


@app.get("/version")
def version():
    """Возвращает версию приложения из переменной окружения APP_VERSION.

    Переменная читается при каждом запросе. Файл .env сам по себе не читается:
    APP_VERSION нужно передать при запуске процесса, иначе вернётся "unknown".
    """
    return {"version": os.getenv("APP_VERSION", "unknown")}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> Item:
    """Добавляет товар в список и возвращает его с кодом 201 Created.

    В item приходит уже проверенный объект: валидацию тела запроса
    выполнил Pydantic до вызова функции.
    """
    items.append(item)
    return item


@app.get("/items")
def list_items() -> list[Item]:
    """Возвращает все товары, добавленные через POST /items с момента запуска."""
    return items
