from typing import Union
import logging

from fastapi import FastAPI

log = logging.getLogger(__name__)


app = FastAPI()

@app.get("/")
def read_root():
    return {"root": "success"}

@app.get("/suite")
def read_run():
    from suite import run
    return run()
    