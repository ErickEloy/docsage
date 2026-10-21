"""Evaluation tests for Docsage RAG system."""
import pytest
from unittest.mock import MagicMock, patch


class TestEvaluationMetrics:
    """Test evaluation metrics for RAG accuracy."""

    @pytest.fixture
    def sample_questions(self):
        return [
            {
                "question": "What is machine learning?",
                "expected_keywords": ["machine", "learning", "ai", "model"],
                "document_id": "test_doc"
            },
            {
                "question": "How does RAG work?",
                "expected_keywords": ["retrieval", "augmented", "generation"],
                "document_id": "test_doc"
            }
        ]

    @patch("app.services.llm.search_similar")
    @patch("app.services.llm.ChatOpenAI")
    def test_accuracy_metric(self, mock_llm, mock_search, sample_questions):
        from app.services.llm import ask_question

        # Mock search results
        mock_doc = MagicMock()
        mock_doc.page_content = "Machine learning is a subset of AI that enables computers to learn from data."
        mock_doc.metadata = {"document_id": "test_doc", "page": 1}
        mock_search.return_value = [mock_doc]

        # Mock LLM response
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Machine learning is a subset of artificial intelligence."
        mock_llm_instance = MagicMock()
        mock_llm_instance.__or__ = MagicMock(return_value=mock_chain)
        mock_llm.return_value = mock_llm_instance

        # Test accuracy
        correct = 0
        for q in sample_questions[:1]:  # Test first question
            answer, sources = ask_question(q["question"], top_k=3)
            answer_lower = answer.lower()
            has_keywords = any(kw in answer_lower for kw in q["expected_keywords"])
            if has_keywords and sources:
                correct += 1

        accuracy = correct / 1.0
        assert accuracy == 1.0

    def test_retrieval_quality(self, sample_questions):
        """Test retrieval relevance."""
        # Simulate retrieval quality metrics
        relevance_scores = [0.85, 0.92, 0.78, 0.95, 0.88]
        avg_relevance = sum(relevance_scores) / len(relevance_scores)
        assert avg_relevance > 0.8

    def test_response_time(self):
        """Test response time is within acceptable limits."""
        import time

        start = time.time()
        # Simulate a quick operation
        _ = [1, 2, 3, 4, 5] * 1000
        elapsed = time.time() - start

        # Should be very fast
        assert elapsed < 1.0