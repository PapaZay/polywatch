from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from services.calibration import compute_calibration

router = APIRouter()

@router.get("/calibration")
def get_calibration(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return compute_calibration(db, category=category)