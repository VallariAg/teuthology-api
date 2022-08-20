from fastapi import APIRouter, HTTPException
from services.suite import run
from schemas.suite import SuiteArgs

router = APIRouter(
    prefix="/suite",
    tags=["suite"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=200)
def create_run(args: SuiteArgs):
    try:
        args = args.dict(by_alias=True)
        run(args)
        return {}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=repr(exc))
