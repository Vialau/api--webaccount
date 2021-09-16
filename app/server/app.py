from fastapi import FastAPI
from .routes import account

app = FastAPI()

app.include_router(account.router, tags=["account"], prefix="/account")


@app.get("/", tags=["Root"])
async def read_root():
    return {"Hello": "World"}
