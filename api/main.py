from fastapi import FastAPI

from routes.author import author_router
from routes.book import book_router
from routes.borrow import borrow_router
from routes.copy import copy_router
from routes.patron import patron_router
from routes.publisher import publisher_router

app = FastAPI()

@app.get("/")
async def greet():
    return {
        "title": "livre",
        "subtitle": "Library Management made easy"
    }

app.include_router(author_router, prefix="/author", tags=["authors"])
app.include_router(book_router, prefix="/book", tags=["books"])
app.include_router(borrow_router, prefix="/borrow", tags=["borrows"])
app.include_router(copy_router, prefix="/copy", tags=["copies"])
app.include_router(patron_router, prefix="/patron", tags=["patrons"])
app.include_router(publisher_router, prefix="/publisher", tags=["publishers"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)