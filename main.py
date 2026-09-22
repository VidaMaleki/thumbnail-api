import os, uuid, logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PIL import Image
from database import engine, Base, get_db
import models, schemas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
app = FastAPI()

PRESETS = {"small": (150, 150), "medium": (400, 400), "large": (800, 800)}
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_target_size(preset: str = None, width: int = None, height: int = None) -> tuple:
    if preset:
        if preset not in PRESETS:
            raise ValueError(f"Invalid preset. Choose from {list(PRESETS.keys())}")
        return PRESETS[preset]
    elif width and height:
        return (width, height)
    else:
        raise ValueError("Must provide either preset or width+height")

@app.post("/thumbnails", response_model=list[schemas.ThumbnailResponse]) 
async def create_thumbnail(
    files: list[UploadFile] = File(...),
    preset: str = Form(None),
    width: int = Form(None),
    height: int = Form(None),
    db: Session = Depends(get_db),
):
    try:
        max_size = get_target_size(preset, width, height)
    except ValueError as e:
        status = 400 if preset else 422
        raise HTTPException(status, str(e))

    results = []
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(422, f"File {file.filename} must be an image")

        file_id = str(uuid.uuid4())
        out_path = f"{UPLOAD_DIR}/{file_id}.jpg"

        image = Image.open(file.file)
        image.thumbnail(max_size)
        image.convert("RGB").save(out_path, "JPEG")

        record = models.Thumbnail(
            id=file_id, original_filename=file.filename,
            preset=preset, width=image.width, height=image.height,
            file_path=out_path,
        )
        db.add(record)
        results.append(record)

    db.commit()
    for r in results:
        db.refresh(r)
    logger.info(f"Created {len(results)} thumbnail(s)")
    return results


@app.get("/thumbnails/{id}", response_model=schemas.ThumbnailResponse)
def get_metadata(id: str, db: Session = Depends(get_db)):
    record = db.query(models.Thumbnail).filter(models.Thumbnail.id == id).first()
    if not record:
        raise HTTPException(404, "Thumbnail not found")
    return record

@app.get("/thumbnails/{id}/download")
def download(id: str, db: Session = Depends(get_db)):
    record = db.query(models.Thumbnail).filter(models.Thumbnail.id == id).first()
    if not record:
        raise HTTPException(404, "Thumbnail not found")
    return FileResponse(record.file_path)


# add /health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}