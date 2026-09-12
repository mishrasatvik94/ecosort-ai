from PIL import Image
import io

def preprocess_image(image_bytes: bytes) -> Image.Image:
    """
    Preprocess uploaded image.
    For MVP, we just load it using PIL and resize it.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # Resize to standard size for a generic model
        image = image.resize((224, 224))
        return image
    except Exception as e:
        raise ValueError(f"Invalid image file: {str(e)}")
