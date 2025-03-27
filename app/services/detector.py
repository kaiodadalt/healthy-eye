import torch
from PIL import Image
import numpy as np
from groundingdino.util.inference import load_model, load_image, predict, annotate
from groundingdino.models import GroundingDINO
import os
import cv2
import traceback
import tempfile

class DetectorService:
    def __init__(self):
        # Check for GPU availability
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Initialize model and config using existing weights
        self.model = load_model(
            "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py",
            "GroundingDINO/weights/groundingdino_swint_ogc.pth"
        )
        # Move model to appropriate device
        self.model.to(self.device)
        
        # More specific text prompt for food detection
        self.TEXT_PROMPT = "chicken, carrot, bean, rice, broccoli, tomato, potato, onion, garlic, meat, fish"
        # Higher thresholds for more confident detections
        self.BOX_THRESHOLD = 0.40  # Increased from 0.25
        self.TEXT_THRESHOLD = 0.35  # Increased from 0.25
        
    def detect(self, image: Image.Image):
        """
        Detect fruits and vegetables in the image.
        
        Args:
            image: PIL Image object
            
        Returns:
            tuple: (list of detected items, list of confidence scores)
        """
        try:
            # Save PIL Image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                image.save(temp_file.name)
                image_path = temp_file.name
            
            # Load image using GroundingDINO's load_image function
            image_source, image = load_image(image_path)
            
            # Run detection
            boxes, logits, phrases = predict(
                model=self.model,
                image=image,
                caption=self.TEXT_PROMPT,
                box_threshold=self.BOX_THRESHOLD,
                text_threshold=self.TEXT_THRESHOLD,
                device=self.device
            )
            
            # Process results
            detected_items = []
            confidence_scores = []
            
            if len(phrases) > 0:
                for phrase, score in zip(phrases, logits):
                    detected_items.append(phrase)
                    confidence_scores.append(float(score))
            
            # Clean up temporary file
            os.unlink(image_path)
            
            return detected_items, confidence_scores
            
        except Exception as e:
            # Get the full traceback
            tb = traceback.format_exc()
            # Get the line number where the error occurred
            error_line = tb.split('\n')[-2].strip()
            
            error_info = {
                "error": "Detection error",
                "message": str(e),
                "type": type(e).__name__,
                "traceback": tb,
                "error_line": error_line,
                "device": self.device,
                "model_path": "GroundingDINO/weights/groundingdino_swint_ogc.pth",
                "config_path": "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
            }
            raise Exception(str(error_info)) 