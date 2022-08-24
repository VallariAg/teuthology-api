from fastapi import APIRouter, HTTPException
from services.suite import run, dry_run
from schemas.suite import SuiteArgs
import logging

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/suite",
    tags=["suite"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=200)
def create_run(args: SuiteArgs):
    try:
        args = args.dict(by_alias=True)
        results = run(args)
        return {"run": results}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))

@router.post("/dryrun", status_code=200)
def create_dryrun(args: SuiteArgs):
    try:
        args = args.dict(by_alias=True)
        result = dry_run(args)
        return result
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))
