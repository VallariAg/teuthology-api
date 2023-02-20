from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from routes import suite, kill, login, logout
from dotenv import load_dotenv
import logging
import os

load_dotenv()

SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')

log = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
def read_root(request: Request):
    return {
        "root": "success",
        "session": request.session.get('user', None)
    }

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)
app.include_router(suite.router)
app.include_router(kill.router)
app.include_router(login.router)
app.include_router(logout.router)
