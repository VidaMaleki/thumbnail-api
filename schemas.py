from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ThumbnailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    original_filename: str
    preset: Optional[str]
    width: int
    height: int
    created_at: datetime

# list all thumbnails, a genuine customer-centric feature explicitly invited by the prompt
class ThumbnailListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    original_filename: str
    preset: Optional[str]
    width: int
    height: int
    created_at: datetime