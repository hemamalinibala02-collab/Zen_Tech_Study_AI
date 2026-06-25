def extract_text(image_file) -> str:
    try:
        from PIL import Image
        import pytesseract
        import os

        # Cloud-safe: do NOT hardcode Windows path
        tesseract_path = os.getenv("TESSERACT_CMD")
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)

        return text.strip() or "(No text detected.)"

    except Exception as e:
        return f"OCR Error: {type(e).__name__}: {e}"
