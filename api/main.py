"""
App for creating summer camp cards and saving them in database.
"""

import uvicorn
from cardmaker import endpoints
from cardmaker.logger import setup_logger
from create_db import create_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="cardmaker")
app.include_router(endpoints.router, prefix="/cardmaker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    setup_logger("my_logger", "app.log")
    create_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
