from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
from app.services.vector_store import search_similar
from typing import List
from pydantic import BaseModel


class Source(BaseModel):
    document_id: str
    page: int
    text: str


SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context from PDF documents.

Rules:
1. Only use information from the provided context to answer.
2. If the context doesn't contain enough information, say so clearly.
3. Always cite the source document and page number for each claim.
4. Be concise but thorough.
5. Answer in the same language as the question.

Context:
{context}"""


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        openai_api_base=settings.openai_base_url,
        temperature=0.1,
    )


def format_context(docs: List) -> str:
    parts = []
    for doc in docs:
        page = doc.metadata.get("page", "N/A")
        document_id = doc.metadata.get("document_id", "unknown")
        parts.append(f"[Document: {document_id}, Page: {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def ask_question(question: str, top_k: int = 5) -> tuple[str, List[Source]]:
    docs = search_similar(question, k=top_k)

    if not docs:
        return "No relevant documents found to answer your question.", []

    context = format_context(docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    llm = get_llm()
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "question": question})

    sources = []
    for doc in docs:
        page = doc.metadata.get("page", 0)
        if isinstance(page, str) and page.isdigit():
            page = int(page)
        elif not isinstance(page, int):
            page = 0
        sources.append(Source(
            document_id=doc.metadata.get("document_id", "unknown"),
            page=page,
            text=doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
        ))

    return answer, sources