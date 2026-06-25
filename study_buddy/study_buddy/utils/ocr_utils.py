def extract_text(image_file) -> str:
    try:
        from PIL import Image
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)

        return text.strip() or "(No text detected.)"

    except Exception as e:
        return (
            f"OCR Error: {type(e).__name__}: {e}"
        )