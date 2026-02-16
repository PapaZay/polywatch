from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.routes.markets import router as market_router
from api.routes.signals import router as signal_router
from api.routes.calibration import router as calibration_router
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import settings
from database import get_db

app = FastAPI(title="Polywatch API, A Polymarket Signal Detector")

app.add_middleware(CORSMiddleware,
                   allow_origins=settings.CORS_ORIGINS.split(","),
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )
app.include_router(market_router, prefix="/api")
app.include_router(signal_router, prefix="/api")
app.include_router(calibration_router, prefix="/api")


@app.get("/")
def get_root():
    return {"status": "API is running..."}



