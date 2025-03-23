from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
from typing import List
from app.models.detection import DetectionResponse
from app.services.detector import DetectorService

handler = APIRouter(
    prefix="/detect",
    tags=["detection"]
)

# Initialize detector service
detector = DetectorService()

@handler.post("", response_model=DetectionResponse)
async def detect_fruits_vegetables(file: UploadFile = File(...)):
    """
    Upload an image and detect fruits and vegetables in it.
    
    Args:
        file: The image file to process
        
    Returns:
        DetectionResponse containing detected items and confidence scores
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Run detection
        detected_items, confidence_scores = detector.detect(image)
        
        return DetectionResponse(
            message="Image processed successfully",
            detected_items=detected_items,
            confidence_scores=confidence_scores
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}") 