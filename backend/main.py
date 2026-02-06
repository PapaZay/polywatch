from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.markets import router as market_router
from api.routes.signals import router as signal_router

app = FastAPI(title="Polywatch API, A Polymarket Signal Detector")

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )
app.include_router(market_router, prefix="/api")
app.include_router(signal_router, prefix="/api")


@app.get("/")
def get_root():
    return {"status": "API is running..."}


@app.get("/health")
def health():
    return {"database": "not connected yet"}
