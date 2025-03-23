from pydantic import BaseModel
from typing import List

class DetectionResponse(BaseModel):
    message: str
    detected_items: List[str]
    confidence_scores: List[float] 