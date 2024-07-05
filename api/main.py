import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cardmaker import endpoints

app = FastAPI()
app.include_router(endpoints.router, prefix="/cardmaker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
