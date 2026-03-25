"""
Tests for the verification logic.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.verification_service import VerificationService
from app.models.schemas import VerificationStatus


class TestVerificationService:
    """Test suite for the verification service."""

    def setup_method(self):
        """Set up mocks before each test."""
        self.mock_pinata = MagicMock()
        self.mock_blockchain = MagicMock()
        self.service = VerificationService(self.mock_pinata, self.mock_blockchain)

    @pytest.mark.asyncio
    async def test_file_not_found(self):
        """Test verification of non-existent file."""
        self.mock_blockchain.file_exists = AsyncMock(return_value=False)

        result = await self.service.verify_and_fetch("nonexistent.pdf")
        assert result["verification"].status == VerificationStatus.NOT_FOUND
        assert result["file_bytes"] is None

    @pytest.mark.asyncio
    async def test_successful_verification(self):
        """Test successful file verification."""
        cid = "QmValidCID123"

        self.mock_blockchain.file_exists = AsyncMock(return_value=True)
        self.mock_blockchain.get_file_cid = AsyncMock(return_value=cid)
        self.mock_blockchain.get_file_record = AsyncMock(
            return_value={
                "cid": cid,
                "timestamp": 1700000000,
                "registered_by": "0xABC",
                "file_type": "image/png",
                "file_size": 1024,
                "exists": True,
            }
        )
        self.mock_blockchain.verify_file = AsyncMock(return_value=True)
        self.mock_pinata.fetch_file = AsyncMock(
            return_value=(b"file content", "image/png")
        )

        result = await self.service.verify_and_fetch("test.png")
        assert result["verification"].status == VerificationStatus.VERIFIED
        assert result["verification"].cids_match is True
        assert result["file_bytes"] == b"file content"

    @pytest.mark.asyncio
    async def test_ipfs_fetch_failure(self):
        """Test behavior when IPFS fetch fails."""
        self.mock_blockchain.file_exists = AsyncMock(return_value=True)
        self.mock_blockchain.get_file_cid = AsyncMock(return_value="QmCID")
        self.mock_blockchain.get_file_record = AsyncMock(
            return_value={
                "cid": "QmCID", "timestamp": 0,
                "registered_by": "0x0", "file_type": "",
                "file_size": 0, "exists": True,
            }
        )
        self.mock_pinata.fetch_file = AsyncMock(
            side_effect=Exception("IPFS timeout")
        )

        result = await self.service.verify_and_fetch("test.png")
        assert result["verification"].status == VerificationStatus.ERROR

    @pytest.mark.asyncio
    async def test_cid_mismatch_detection(self):
        """Test that CID mismatch is detected (tampering)."""
        self.mock_blockchain.file_exists = AsyncMock(return_value=True)
        self.mock_blockchain.get_file_cid = AsyncMock(return_value="QmRealCID")

        result = await self.service.verify_only("test.png", "QmTamperedCID")
        assert result.status == VerificationStatus.TAMPERED
        assert result.cids_match is False
