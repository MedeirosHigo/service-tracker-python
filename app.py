# app.py
import resource
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ocr_tesseract import extract_text_from_path
import uvicorn

limit = 256 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_AS, (limit, limit))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    temp_dir = "./image"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, "temp_img.jpg")
    try:
        with open(temp_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)
        text = extract_text_from_path(temp_path, lang="fra")
        os.remove(temp_path)
        return JSONResponse({"text": text})
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=1)
