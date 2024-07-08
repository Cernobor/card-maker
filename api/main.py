"""
App for creating summer camp cards and saving them in database.
"""

import os
import uvicorn
from cardmaker import endpoints
from create_db import create_db
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex


api = FastAPI(title="api")
api.include_router(endpoints.router)

client_files = SPAStaticFiles(directory=os.getenv("CLIENT_FILES", "/client"))

app = FastAPI(title="cardmaker")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.mount("/api", api)
app.mount("/", client_files)

if __name__ == "__main__":
    create_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
