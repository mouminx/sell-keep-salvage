import os
from backend.ocr.parser import extract_text

def test_extract_text():
    """Ensure OCR extracts readable text lines from a sample image."""
    sample_path = "data/samples/tooltip.png"
    assert os.path.exists(sample_path), "Sample image not found"

    text_lines = extract_text(sample_path)
    assert isinstance(text_lines, list)
    assert len(text_lines) > 0, "No text detected"

    print("\n[DEBUG] OCR output:")
    for line in text_lines:
        print(" >", line)
