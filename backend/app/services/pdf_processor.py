from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings
from typing import List
from langchain_core.documents import Document


def process_pdf(file_path: str, document_id: str) -> tuple[int, List[Document]]:
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents(pages)
    for i, chunk in enumerate(chunks):
        chunk.metadata["document_id"] = document_id
        chunk.metadata["chunk_index"] = i

    return len(pages), chunks