from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
from datetime import datetime

class JobStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class JobOut(BaseModel):
    id: int
    filename: str
    status: JobStatus
    total_rows: int
    processed: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
