import torch
from PIL import Image
import numpy as np
from groundingdino.util.inference import load_model, predict
from groundingdino.models import GroundingDINO
import os
import cv2
import traceback

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
        
        self.TEXT_PROMPT = "broccoli, carrot, tomato, chicken, rice, beans"
        self.BOX_THRESHOLD = 0.35
        self.TEXT_THRESHOLD = 0.25
        
    def detect(self, image: Image.Image):
        """
        Detect fruits and vegetables in the image.
        
        Args:
            image: PIL Image object
            
        Returns:
            tuple: (list of detected items, list of confidence scores)
        """
        try:
            # Convert PIL Image to numpy array
            image_np = np.array(image)
            
            # Ensure image is in RGB format
            if len(image_np.shape) == 2:  # Grayscale
                image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
            elif image_np.shape[2] == 4:  # RGBA
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
            
            # Resize image if too large (max dimension 800px)
            max_dim = 800
            h, w = image_np.shape[:2]
            if max(h, w) > max_dim:
                scale = max_dim / max(h, w)
                new_h, new_w = int(h * scale), int(w * scale)
                image_np = cv2.resize(image_np, (new_w, new_h))
            
            # Convert RGB to BGR for OpenCV
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            # Convert numpy array to tensor and normalize
            image_tensor = torch.from_numpy(image_np).float()
            image_tensor = image_tensor / 255.0
            image_tensor = image_tensor.permute(2, 0, 1)  # HWC to CHW
            image_tensor = image_tensor.to(self.device)
            
            # Run detection
            boxes, logits, phrases = predict(
                model=self.model,
                image=image_tensor,
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