from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
from typing import List, Dict, Any
from app.models.detection import DetectionResponse
from app.services.detector import DetectorService
import traceback

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
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid file type",
                "message": f"File must be an image. Received content type: {file.content_type}",
                "type": "ValidationError"
            }
        )
    
    try:
        # Read and validate image
        contents = await file.read()
        if not contents:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Empty file",
                    "message": "Empty file received",
                    "type": "ValidationError"
                }
            )
            
        # Try to open the image to validate it
        try:
            image = Image.open(io.BytesIO(contents))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid image",
                    "message": f"Invalid image file: {str(e)}",
                    "type": "ValidationError"
                }
            )
        
        # Run detection
        detected_items, confidence_scores = detector.detect(image)
        
        if not detected_items:
            return DetectionResponse(
                message="No fruits or vegetables detected in the image",
                detected_items=[],
                confidence_scores=[]
            )
        
        return DetectionResponse(
            message="Image processed successfully",
            detected_items=detected_items,
            confidence_scores=confidence_scores
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Get the full traceback
        tb = traceback.format_exc()
        # Get the line number where the error occurred
        error_line = tb.split('\n')[-2].strip()
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Detection error",
                "message": str(e),
                "type": type(e).__name__,
                "traceback": tb,
                "error_line": error_line
            }
        ) 