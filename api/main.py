"""
App for creating summer camp cards and saving them in database.
"""

import uvicorn
from cardmaker import endpoints
from cardmaker.logger import Logger
from create_db import create_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
import time
from http.client import responses

logger = Logger.get_instance()

app = FastAPI(title="api")
app.include_router(endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log(request: Request, call_next: RequestResponseEndpoint):
    # Log request details
    client_ip = request.client.host
    client_port = request.client.port
    method = request.method
    url = request.url
    headers = request.headers

    t0 = time.time()
    # Process the request
    response = await call_next(request)
    t = time.time() - t0

    # Log response details
    status_code = response.status_code
    logger.info(f'REQ: {client_ip}:{client_port} {method} {url} {headers} RES: {status_code} {responses[status_code]} dur={int(1000*t)}ms')

    return response

if __name__ == "__main__":
    create_db()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8003,
        log_config=None,
    )
