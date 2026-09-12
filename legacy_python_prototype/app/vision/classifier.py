import random
from typing import Tuple
from PIL import Image

class PrototypeDemonstrationClassifier:
    def __init__(self, categories: list):
        """
        categories: list of category names (strings)
        """
        self.categories = categories
        # A deterministic mapping based on filename to guarantee reliable demo behavior without GPUs
        self.mock_mapping = {
            "banana": ("Organic", 0.92),
            "apple": ("Organic", 0.88),
            "bottle": ("Plastic", 0.85),
            "mobile": ("E-Waste", 0.96),
            "battery": ("E-Waste", 0.95),
            "box": ("Paper", 0.82),
            "bleach": ("Hazardous", 0.90),
            "diaper": ("Sanitary", 0.89),
            "glass": ("Glass", 0.84),
            "paper": ("Paper", 0.87),
            "can": ("Metal", 0.81),
            "unknown": ("Other/Unknown", 0.30), # Force low confidence
            "blurry": ("Other/Unknown", 0.45) # Force uncertain
        }

    def predict(self, image: Image.Image, filename: str = "") -> Tuple[str, float]:
        """
        Returns (predicted_category, confidence)
        """
        filename_lower = filename.lower()
        
        # Check for heuristics
        for key, (cat, conf) in self.mock_mapping.items():
            if key in filename_lower:
                return cat, conf
        
        # Fallback for untested images
        cat = random.choice(self.categories)
        conf = round(random.uniform(0.4, 0.99), 2)
        return cat, conf
