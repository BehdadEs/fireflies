from fastapi import FastAPI, HTTPException, status
from database import models
from database.db import engine
from routers import admin, mock, log

models.Base.metadata.create_all(bind=engine)


app = FastAPI(redoc_url=None, debug=False)


@app.get("/")
def root():
    return {"Fireflies": "Look For the Light"}


app.include_router(admin.router)
app.include_router(log.router)
app.include_router(mock.router)
