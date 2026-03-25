"""
Tests for the retrieval endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app
from app.models.schemas import VerificationStatus

client = TestClient(app)


class TestRetrieveEndpoint:
    """Test suite for GET /api/v1/file/{file_name}"""

    @patch("app.routers.retrieve.VerificationService")
    def test_successful_retrieval(self, mock_verifier_cls):
        """Test successful file retrieval and verification."""
        mock_verifier = MagicMock()
        mock_verifier.verify_and_fetch = AsyncMock(
            return_value={
                "verification": MagicMock(
                    status=VerificationStatus.VERIFIED,
                    blockchain_cid="QmCID123",
                    registered_by="0xABC",
                    timestamp="2024-01-01",
                ),
                "file_bytes": b"file content",
                "content_type": "text/plain",
            }
        )
        mock_verifier_cls.return_value = mock_verifier

        response = client.get("/api/v1/file/test.txt")

        assert response.status_code == 200
        assert response.content == b"file content"
        assert response.headers["X-ChainGuard-Status"] == "verified"

    @patch("app.routers.retrieve.VerificationService")
    def test_file_not_found(self, mock_verifier_cls):
        """Test retrieval of non-existent file."""
        mock_verifier = MagicMock()
        mock_verifier.verify_and_fetch = AsyncMock(
            return_value={
                "verification": MagicMock(
                    status=VerificationStatus.NOT_FOUND,
                    message="File not found",
                ),
                "file_bytes": None,
            }
        )
        mock_verifier_cls.return_value = mock_verifier

        response = client.get("/api/v1/file/nonexistent.txt")

        assert response.status_code == 404

    @patch("app.routers.retrieve.VerificationService")
    def test_tampering_detected(self, mock_verifier_cls):
        """Test detection of file tampering."""
        mock_verifier = MagicMock()
        mock_verifier.verify_and_fetch = AsyncMock(
            return_value={
                "verification": MagicMock(
                    status=VerificationStatus.TAMPERED,
                    message="File has been tampered with",
                ),
                "file_bytes": None,
            }
        )
        mock_verifier_cls.return_value = mock_verifier

        response = client.get("/api/v1/file/tampered.txt")

        assert response.status_code == 409
