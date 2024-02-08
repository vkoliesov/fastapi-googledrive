import uvicorn

from fastapi import FastAPI
from api.routers import api_router


app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
