from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
import logging

log = logging.getLogger(__name__)
router = APIRouter(
    prefix="/logout",
    tags=["logout"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', status_code=200)
def logout(request: Request):
    request.session.pop('user', None)
    return {
        "logout": "success"
    }