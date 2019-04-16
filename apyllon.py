import logging
from logging.config import dictConfig

from logger import logging_config

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

from backend.routers import (
    player,
    users,
)
import backend_database as bd
from backend.player import player_


@app.on_event("startup")
async def startup():
    db = bd.Session()
    pw = await bd.create_first_user(db)
    if pw:
        # Note: This print only works on 20 character passwords
        print(f'''
################################################################################
#                    Copy this Password and login as admin.                    #
#                  After that immediately change the password!                 #
#                                                                              #
#                             {pw}                             #
#                                                                              #
################################################################################''')
    # # TODO:  This is just done for mocking
    await player_.add_youtube('https://www.youtube.com/watch?v=PXbU_UI-lAg', db=db)
    await player_.add_youtube('https://www.youtube.com/watch?v=LBZ-3Ugj1AQ', db=db)
    await player_.add_youtube('https://www.youtube.com/watch?v=U5u9glfqDsc', db=db)
    db.close()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.middleware("http")
async def db_session_middleware(
        request: Request,
        call_next
):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = bd.Session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(users.router)
app.include_router(player.router)
