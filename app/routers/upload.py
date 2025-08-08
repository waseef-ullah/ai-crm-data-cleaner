from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import os
from pathlib import Path
from app.tasks import process_upload
from app.models import Job

router = APIRouter()

UPLOAD_FOLDER = Path("/data/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@router.post("/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX supported in MVP")

    save_path = UPLOAD_FOLDER / file.filename
    with save_path.open("wb") as f:
        content = await file.read()
        f.write(content)

    db: Session = SessionLocal()
    job = models.Job(filename=file.filename, status="pending")
    db.add(job); db.commit(); db.refresh(job)

    # enqueue celery task
    process_upload.delay(job.id, str(save_path))

    db.close()
    return {"job_id": job.id}
