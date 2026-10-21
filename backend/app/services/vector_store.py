from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings
from langchain_core.documents import Document
from typing import List, Optional


_embeddings = None
_vector_store = None


def get_embeddings() -> OpenAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
            openai_api_base=settings.openai_base_url,
        )
    return _embeddings


def get_vector_store() -> Chroma:
    global _vector_store
    if _vector_store is None:
        _vector_store = Chroma(
            collection_name="docsage",
            embedding_function=get_embeddings(),
            persist_directory=settings.chroma_persist_directory,
        )
    return _vector_store


def add_documents(documents: List[Document]) -> None:
    vector_store = get_vector_store()
    vector_store.add_documents(documents)


def search_similar(query: str, k: int = 5) -> List[Document]:
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=k)


def reset_vector_store() -> None:
    global _vector_store
    if _vector_store is not None:
        _vector_store.delete_collection()
        _vector_store = None