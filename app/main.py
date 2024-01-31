import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv()

from app.api import router
from app.db import models
from app.db.database import engine
print("Finish load env")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Web App",
    description="Map Web App",
    version="0.0.1"
)
# # Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

app.include_router(router)

app.mount("/", StaticFiles(directory="./app/dist", html=True), name="frontend")
