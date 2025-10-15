import cv2
import numpy as np

def clean_image(image_path: str):
    """
    enhanced preprocessing for diablo-style tooltips
    - converts to grayscale
    - boosts contrast
    - removes noise
    - sharpens edges
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    #convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #contrast limited adaptive histogram equalizer (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    
    #denoise slightly
    gray = cv2.medianBlur(gray, 3)
    
    #sharpen text edges
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    gray = cv2.filter2D(gray, -1, kernel)
    
    #threshold (optional for better clarity)
    _, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    
    return binary