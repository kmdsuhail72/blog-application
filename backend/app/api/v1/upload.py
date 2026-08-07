import os
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_COVER_FILE = File(...)


def _write_file(file_path: str, contents: bytes) -> None:
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "uploads", "covers"
)
VALID_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/cover")
async def upload_cover(file: UploadFile = UPLOAD_COVER_FILE):
    if file.content_type not in VALID_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only JPEG, PNG, and WEBP are allowed.",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 5 MB.",
        )

    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in {"jpg", "jpeg", "png", "webp"}:
        file_extension = file.content_type.split("/")[-1]

    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    await run_in_threadpool(_write_file, file_path, contents)

    url = f"/uploads/covers/{filename}"
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"url": url})
