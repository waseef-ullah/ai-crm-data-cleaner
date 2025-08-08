import os
import pandas as pd
from app.celery_worker import celery_app
from app.database import SessionLocal, engine
from app import models
from app.cleaning import process_dataframe
from sqlalchemy.orm import Session
from io import BytesIO
import json

@celery_app.task(bind=True)
def process_upload(self, job_id: int, file_path: str):
    db: Session = SessionLocal()
    try:
        job = db.query(models.Job).get(job_id)
        if not job:
            return {"error": "job not found"}
        job.status = "in_progress"
        db.add(job); db.commit()

        # read csv
        df = pd.read_csv(file_path)
        job.total_rows = len(df)
        db.add(job); db.commit()

        # store raw rows
        for row in df.fillna("").to_dict(orient="records"):
            rc = models.RawContact(job_id=job_id, data=row)
            db.add(rc)
        db.commit()

        cleaned = process_dataframe(df)

        # store cleaned
        for row in cleaned:
            cc = models.CleanedContact(job_id=job_id, data=row)
            db.add(cc)
        db.commit()

        job.processed = len(cleaned)
        job.status = "completed"
        job.result = {"cleaned_rows": len(cleaned)}
        db.add(job); db.commit()
        return {"status": "completed"}
    except Exception as e:
        job = db.query(models.Job).get(job_id)
        if job:
            job.status = "failed"
            job.error = str(e)
            db.add(job); db.commit()
        return {"error": str(e)}
    finally:
        db.close()
