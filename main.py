from os import path
from unittest.mock import patch
from fastapi import FastAPI
import uvicorn

app = FastAPI(debug=True)


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = []


@app.get("/books")
async def read_all_books():
    return BOOKS


if __name__ == "__main__":
    uvicorn.run("main:app")
