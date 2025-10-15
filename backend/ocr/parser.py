import os
import cv2
import pytesseract
from backend.utils.preprocessing import clean_image

#optional: set tesseract path only if on windows
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path: str):
    #extract readable text lines from an image using tesseract ocr
    #applies preprocessing for cleaner results
    
    #step 1: load + preprocess the image
    img =  clean_image(image_path)
    
    #step 2: ocr extraction
    text = pytesseract.image_to_string(img)
    
    #step 3: split and clean up lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    return lines

if __name__ == "__main__":
    import os
    import cv2

    test_path = "data/samples/tooltip.png"
    try:
        img = clean_image(test_path)
        os.makedirs("data/debug", exist_ok=True)
        cv2.imwrite("data/debug/preprocessed.png", img)
        
        lines = extract_text(test_path)
        print("\n OCR Test Output:")
        for line in lines:
            print(" >", line)
            
    except Exception as e:
        print("\n OCR test failed:", e)
