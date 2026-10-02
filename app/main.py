from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(

    title="FitBuddy - AI Fitness Plan Generator",

    description=(
        "AI-powered personalized fitness "
        "plan generation system."
    ),

    version="1.0.0",

    lifespan=lifespan

)


BASE_DIR = Path(__file__).resolve().parent


app.mount(

    "/static",

    StaticFiles(
        directory=str(
            BASE_DIR / "static"
        )
    ),

    name="static"

)


app.include_router(router)


@app.get("/health")
def health():

    return {

        "status": "ok",

        "service": "FitBuddy",

        "message": "FitBuddy API is running"

    }