import logging
from fastapi import FastAPI

from routes import suite, kill

log = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
def read_root():
    return {"root": "success"}

app.include_router(suite.router)
app.include_router(kill.router)
