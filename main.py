from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
import uvicorn


app = FastAPI(debug=True)


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


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
    published_date: int = Field(gt=1999, lt=2031)

    class Config:  # pydantic class
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "Codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2030),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2030),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2029),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2028),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2027),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# path param
@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):  # data validation for path params
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


# query param
@app.get("/book/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(
    book_rating: int = Query(gt=0, lt=6)
):  # data validation for query params
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


# query param
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(
    published_date: int = Query(gt=1999, lt=2031)
):  # data validation for query params
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
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


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book  # type: ignore
            book_changed = True
    if not book_changed:  # raising an error
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete(
    "/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT
)  # data validation for path params
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:  # raising an error
        raise HTTPException(status_code=404, detail="item not found")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
