from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from services.upload_service import process_pdf

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):

    result = process_pdf(file, db)
    print()

    return result