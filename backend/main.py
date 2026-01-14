from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Polywatch API, A Polymarket Signal Detector")

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

@app.get("/")
def get_root():
    return {"status": "API is running..."}
@app.get("/health")
def health():
    return {"database": "not connected yet"}
