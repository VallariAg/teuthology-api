import logging
from fastapi import FastAPI

from routes import suite, queue
from config import settings

log = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
def read_root():
    return {"root": "success"}


@app.get("/config")
def read_root():
    # k = os.environ("PADDLES_ADDRESS")
    return {"settings": settings, "k": "k"}

app.include_router(suite.router)
app.include_router(queue.router)
