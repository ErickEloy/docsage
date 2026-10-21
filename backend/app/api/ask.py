from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.services.vector_store import get_vector_store
from app.services.llm import ask_question

router = APIRouter()


class Source(BaseModel):
    document_id: str
    page: int
    text: str


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


class AskResponse(BaseModel):
    answer: str
    sources: List[Source]


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    vector_store = get_vector_store()
    if vector_store._collection.count() == 0:
        raise HTTPException(status_code=400, detail="No documents indexed. Please upload a PDF first.")

    try:
        answer, sources = ask_question(request.question, request.top_k)
        return AskResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")