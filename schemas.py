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