"""
Tests for the upload endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app

client = TestClient(app)


class TestUploadEndpoint:
    """Test suite for POST /api/v1/upload"""

    @patch("app.routers.upload.BlockchainService")
    @patch("app.routers.upload.PinataService")
    def test_successful_upload(self, mock_pinata_cls, mock_blockchain_cls):
        """Test successful file upload flow."""
        mock_pinata = MagicMock()
        mock_pinata.upload_file = AsyncMock(
            return_value=("QmTestCID123456789abcdef", 1024)
        )
        mock_pinata.get_gateway_url.return_value = (
            "https://gateway.pinata.cloud/ipfs/QmTestCID123456789abcdef"
        )
        mock_pinata_cls.return_value = mock_pinata

        mock_blockchain = MagicMock()
        mock_blockchain.register_file = AsyncMock(
            return_value={
                "transaction_hash": "0xabc123",
                "block_number": 12345,
                "gas_used": 50000,
                "status": "confirmed",
            }
        )
        mock_blockchain_cls.return_value = mock_blockchain

        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.png", b"fake image content", "image/png")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["ipfs_cid"] == "QmTestCID123456789abcdef"
        assert data["transaction_hash"] == "0xabc123"

    def test_empty_file_rejected(self):
        """Test that empty files are rejected."""
        response = client.post(
            "/api/v1/upload",
            files={"file": ("empty.txt", b"", "text/plain")},
        )
        assert response.status_code == 400

    def test_no_file_rejected(self):
        """Test that requests without files are rejected."""
        response = client.post("/api/v1/upload")
        assert response.status_code == 422
