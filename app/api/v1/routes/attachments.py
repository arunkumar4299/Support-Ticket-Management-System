from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter(
    prefix="/attachments",
    tags=["Attachments"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
    ".txt",
    ".doc",
    ".docx",
}


@router.post("/upload")
async def upload_attachment(file: UploadFile = File(...)):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type is not allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    content = await file.read()

    file_path.write_bytes(content)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "file_path": str(file_path),
        "size": len(content)
    }


@router.get("/")
def get_attachments():
    files = []

    for file in UPLOAD_DIR.iterdir():
        if file.is_file():
            files.append({
                "filename": file.name,
                "file_path": str(file)
            })

    return {
        "attachments": files
    }