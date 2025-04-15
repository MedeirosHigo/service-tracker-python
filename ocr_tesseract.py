# ocr_tesseract.py
from PIL import Image
import pytesseract
from preprocess import preprocess_image

def extract_text_from_path(img_path: str, lang: str = "fra") -> str:
    preprocess_image(img_path)
    img = Image.open(img_path)
    raw = pytesseract.image_to_string(img, lang=lang)
    return " ".join(raw.split())
