from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
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


class BookRequest(BaseModel):
    # if an id is not passed in the body, it receives None value
    # id: Optional[int] = None  # -> suficiente para ser opcional
    id: Optional[int] = Field(
        default=None,
        title="this is not needed",
        description="id is not needed(description)",
    )
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    class Config:  # pydantic class
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "Codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5),
    Book(4, "HP1", "Author 1", "Book Description", 2),
    Book(5, "HP2", "Author 2", "Book Description", 3),
    Book(6, "HP3", "Author 3", "Book Description", 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


# find and assign a new id to a book
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    return book


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
