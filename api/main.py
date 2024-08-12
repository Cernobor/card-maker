"""
App for creating summer camp cards and saving them in database.
"""

import uvicorn
from cardmaker import endpoints
from create_db import create_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="api")
app.include_router(endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    create_db()
    uvicorn.run(app, host="0.0.0.0", port=8003)
