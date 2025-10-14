import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from backend.utils.preprocessing import preprocess_image

def extract_text(image_path):
    img = preprocess_image(cv2.imread(image_path))
    text = pytesseract.image_to_string(img)
    return text.splitlines()