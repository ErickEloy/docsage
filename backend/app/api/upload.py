from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os

from app.config import settings
from app.services.pdf_processor import process_pdf
from app.services.vector_store import get_vector_store, add_documents

router = APIRouter()


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    pages: int
    chunks: int
    message: str


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    document_id = str(uuid.uuid4())
    upload_dir = os.path.join(settings.chroma_persist_directory, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{document_id}.pdf")

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        pages, chunks = process_pdf(file_path, document_id)
        add_documents(chunks)
        return UploadResponse(
            document_id=document_id,
            filename=file.filename,
            pages=pages,
            chunks=len(chunks),
            message="PDF processed and indexed successfully",
        )
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")