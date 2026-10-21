import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setenv("CHROMA_PERSIST_DIRECTORY", "./test_chroma_data")


class TestConfig:
    def test_settings_load(self, monkeypatch):
        from app.config import settings
        assert settings.chunk_size == 1000
        assert settings.chunk_overlap == 200


class TestPDFProcessor:
    @patch("app.services.pdf_processor.PyPDFLoader")
    def test_process_pdf(self, mock_loader, monkeypatch):
        from app.services.pdf_processor import process_pdf

        mock_page = MagicMock()
        mock_page.page_content = "Test page content"
        mock_page.metadata = {"page": 1}
        mock_loader.return_value.load.return_value = [mock_page, mock_page]

        pages, chunks = process_pdf("test.pdf", "doc-123")

        assert pages == 2
        assert len(chunks) > 0
        assert all("document_id" in chunk.metadata for chunk in chunks)
        assert all(chunk.metadata["document_id"] == "doc-123" for chunk in chunks)


class TestHealthAPI:
    @pytest.mark.asyncio
    async def test_health_check(self):
        from app.api.health import health_check

        result = await health_check()
        assert result["status"] == "ok"
        assert result["service"] == "docsage-api"


class TestAskAPI:
    @pytest.mark.asyncio
    async def test_ask_empty_question(self):
        from app.api.ask import ask, AskRequest
        from fastapi import HTTPException

        request = AskRequest(question="")

        with pytest.raises(HTTPException) as exc:
            await ask(request)
        assert exc.value.status_code == 400


class TestUploadAPI:
    @pytest.mark.asyncio
    async def test_upload_invalid_file(self):
        from app.api.upload import UploadResponse
        from fastapi import HTTPException
        from unittest.mock import AsyncMock, MagicMock

        file_mock = MagicMock()
        file_mock.filename = "test.txt"
        file_mock.read = AsyncMock()

        from app.api.upload import upload_pdf
        with pytest.raises(HTTPException) as exc:
            await upload_pdf(file_mock)
        assert exc.value.status_code == 400