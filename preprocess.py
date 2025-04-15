from PIL import Image

def preprocess_image(img_path: str, size=(900, 720)):
    with Image.open(img_path) as img:
        img = img.resize(size, Image.LANCZOS)
        img = img.convert("L")
        img.save(img_path)
