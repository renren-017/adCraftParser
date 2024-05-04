from fastapi import FastAPI
from app.routes.categories import router as api_router

app = FastAPI()

app.include_router(api_router)
