import logging
from fastapi import FastAPI, HTTPException

from suite import run
from schemas.suite import SuiteArgs


log = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
def read_root():
    return {"root": "success"}

@app.post("/suite", status_code=200)
def create_run(args: SuiteArgs):
    try:
        args = args.dict(by_alias=True)
        run(args)
        return {}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))
