import logging
import os
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import httpx

load_dotenv()

GH_CLIENT_ID = os.getenv('GH_CLIENT_ID')
GH_CLIENT_SECRET = os.getenv('GH_CLIENT_SECRET')
GH_AUTHORIZATION_BASE_URL = os.getenv('GH_AUTHORIZATION_BASE_URL')
GH_TOKEN_URL = os.getenv('GH_TOKEN_URL')
GH_FETCH_MEMBERSHIP_URL = os.getenv('GH_FETCH_MEMBERSHIP_URL')

log = logging.getLogger(__name__)
router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200)
async def github_login():
    """
    GET route for /login, (If first time) will redirect to github login page
    where you should authorize the app to gain access.
    """
    scope = 'read:org'
    return RedirectResponse(
        f'{GH_AUTHORIZATION_BASE_URL}?client_id={GH_CLIENT_ID}&scope={scope}',
        status_code=302
    )

@router.get("/callback", status_code=200)
async def handle_callback(code: str, request: Request):
    """
    Call back route after user login & authorize the app
    for access.
    """
    params = {
        'client_id': GH_CLIENT_ID,
        'client_secret': GH_CLIENT_SECRET,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as client:
        response_token = await client.post(url=GH_TOKEN_URL, params=params, headers=headers)
        log.info(response_token.json())
        response_token_dic = dict(response_token.json())
        token = response_token_dic.get('access_token')
        if response_token_dic.get('error') or not token:
            log.error("The code is incorrect or expired.")
            raise HTTPException(
                status_code=401, detail="The code is incorrect or expired.")
        headers = {'Authorization': 'token ' + token}
        response_org = await client.get(url=GH_FETCH_MEMBERSHIP_URL, headers=headers)
        log.info(response_org.json())
        if response_org.status_code == 404:
            log.error("User is not part of the Ceph Organization")
            raise HTTPException(
                status_code=404,
                detail="User is not part of the Ceph Organization, please contact <admin>"
            )
        if response_org.status_code == 403:
            log.error("The application doesn't have permission to view github org")
            raise HTTPException(
                status_code=403,
                detail="The application doesn't have permission to view github org"
            )
        response_org_dic = dict(response_org.json())
        data = {
            "id": response_org_dic.get('user', {}).get('id'),
            "username": response_org_dic.get('user', {}).get('login'),
            "state": response_org_dic.get('state'),
            "role": response_org_dic.get('role'),
            "access_token": token,
        }
        request.session['user'] = data
    return RedirectResponse(url='/')
