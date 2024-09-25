from fastapi import FastAPI
from routers.author import author_router
from routers.patron import patron_router
from routers.publisher import publisher_router
from routers.borrow import borrow_router
from routers.copy import copy_router
from routers.book import book_router
from database import init_db

app = FastAPI()

app.include_router(author_router, prefix="/author")
app.include_router(book_router, prefix="/book")
app.include_router(patron_router, prefix="/patron")
app.include_router(publisher_router, prefix="/publisher")
app.include_router(borrow_router, prefix="/borrow")
app.include_router(copy_router, prefix="/copy")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def greet():
    return {"message": "livre says hello!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)