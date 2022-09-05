from fastapi import APIRouter, HTTPException
from services.queue import run
from schemas.queue import QueueArgs
import logging

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/queue",
    tags=["queue"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=200)
def create_run(args: QueueArgs, delete: str = None, pause: int = None):
    try:
        args = args.dict(by_alias=True)
        results = run(args, delete, pause)
        return results
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))
