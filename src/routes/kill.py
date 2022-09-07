from fastapi import APIRouter, HTTPException
from services.kill import run
from schemas.kill import KillArgs

import logging

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/kill",
    tags=["kill"],
)

@router.post("/", status_code=200)
def create_run(args: KillArgs, access_token: str, logs: bool = False):
    """
    access_token should be of format `<token-type> <token>`
    Example: "bearer <token>"
    """
    try:
        args = args.dict(by_alias=True)
        results = run(args, logs, access_token)
        return results
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))
