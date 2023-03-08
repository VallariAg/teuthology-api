from fastapi import APIRouter, HTTPException
from services.suite import run
from schemas.suite import SuiteArgs
import logging

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/suite",
    tags=["suite"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=200)
def create_run(args: SuiteArgs, dry_run: bool = False, logs: bool = False):
    try:
        args = args.dict(by_alias=True)
        results = run(args, dry_run, logs)
        return results
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))
