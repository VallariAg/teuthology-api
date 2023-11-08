import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from teuthology_api.config import settings

PULPITO_URL = settings.pulpito_url
log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/logout",
    tags=["logout"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200)
def logout(request: Request):
    """
    GET route for logging out.
    """
    user = request.session.get("user")
    if user:
        request.session.pop("user", None)
        return RedirectResponse(PULPITO_URL)
    log.warning("No session found, probably already logged out.")
    raise HTTPException(
        status_code=204, detail="No session found, probably already logged out."
    )
