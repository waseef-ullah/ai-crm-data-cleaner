from fastapi import FastAPI
from app.routers import upload, jobs
import uvicorn

app = FastAPI(title="AI CRM Data Cleaner")

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
