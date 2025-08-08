from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app import models
from fastapi.responses import StreamingResponse
import csv, io
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/{job_id}")
def get_job(job_id: int):
    db: Session = SessionLocal()
    job = db.query(models.Job).get(job_id)
    db.close()
    if not job:
        raise HTTPException(404, "job not found")
    return {
        "id": job.id,
        "filename": job.filename,
        "status": job.status,
        "total_rows": job.total_rows,
        "processed": job.processed,
        "result": job.result,
        "error": job.error
    }

@router.get("/{job_id}/download")
def download_cleaned(job_id: int):
    db: Session = SessionLocal()
    job = db.query(models.Job).get(job_id)
    if not job:
        db.close()
        raise HTTPException(404, "job not found")
    rows = db.query(models.CleanedContact).filter_by(job_id=job_id).all()
    db.close()
    if not rows:
        raise HTTPException(404, "no cleaned data")

    # stream CSV
    stream = io.StringIO()
    writer = None
    for r in rows:
        data = r.data
        if writer is None:
            writer = csv.DictWriter(stream, fieldnames=list(data.keys()))
            writer.writeheader()
        writer.writerow(data)
    stream.seek(0)
    return StreamingResponse(iter([stream.getvalue()]), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=cleaned_{job.filename}"})
