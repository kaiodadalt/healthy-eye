import os
import torch
from groundingdino.util.inference import load_model, load_image, predict
from groundingdino.util.utils import get_phrases_from_posmap
import numpy as np

class DetectorService:
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.text_prompt = "fruit vegetable food produce"
        self.box_threshold = 0.35
        self.text_threshold = 0.25
        
    def initialize_model(self):
        """Initialize the GroundingDINO model"""
        if self.model is None:
            config_path = os.path.join("GroundingDINO", "groundingdino", "config", "GroundingDINO_SwinT_OGC.py")
            weights_path = os.path.join("GroundingDINO", "weights", "groundingdino_swint_ogc.pth")
            
            # Download weights if they don't exist
            if not os.path.exists(weights_path):
                os.makedirs(os.path.dirname(weights_path), exist_ok=True)
                import urllib.request
                url = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"
                urllib.request.urlretrieve(url, weights_path)
            
            self.model = load_model(config_path, weights_path, device=self.device)
    
    def detect(self, image):
        """Detect fruits and vegetables in the image"""
        if self.model is None:
            self.initialize_model()
            
        # Load and preprocess image
        image_source, image = load_image(image)
        
        # Run detection
        boxes, logits, phrases = predict(
            model=self.model,
            image=image,
            caption=self.text_prompt,
            box_threshold=self.box_threshold,
            text_threshold=self.text_threshold,
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