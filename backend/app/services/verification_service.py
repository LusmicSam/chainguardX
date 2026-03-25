"""
Core verification logic.
"""

import logging
from app.services.pinata_service import PinataService
from app.services.blockchain_service import BlockchainService
from app.models.schemas import VerificationResult, VerificationStatus
from app.utils.hashing import compute_sha256, verify_cid_match

logger = logging.getLogger(__name__)


class VerificationService:
    """Orchestrates the file integrity verification process."""

    def __init__(
        self,
        pinata_service: PinataService,
        blockchain_service: BlockchainService
    ):
        self.pinata = pinata_service
        self.blockchain = blockchain_service

    async def verify_and_fetch(self, file_name: str) -> dict:
        """Complete verification and fetch workflow."""
        logger.info(f"=== VERIFICATION START: {file_name} ===")
        
        exists = await self.blockchain.file_exists(file_name)

        if not exists:
            logger.warning(f"File '{file_name}' not found on blockchain")
            return {
                "verification": VerificationResult(
                    status=VerificationStatus.NOT_FOUND,
                    file_name=file_name,
                    cids_match=False,
                    message=f"File '{file_name}' is not registered on the blockchain"
                ),
                "file_bytes": None,
                "content_type": None
            }

        logger.info("Step 2: Querying blockchain for trusted CID...")
        blockchain_cid = await self.blockchain.get_file_cid(file_name)
        logger.info(f"  Blockchain CID: {blockchain_cid}")

        logger.info("Step 3: Getting full file record...")
        record = await self.blockchain.get_file_record(file_name)
        logger.info(f"  Registered by: {record['registered_by']}")
        logger.info(f"  Timestamp: {record['timestamp']}")

        logger.info("Step 4: Fetching file from IPFS...")
        try:
            file_bytes, content_type = await self.pinata.fetch_file(blockchain_cid)
            logger.info(f"  Fetched {len(file_bytes)} bytes, type: {content_type}")
        except Exception as e:
            logger.error(f"  IPFS fetch failed: {e}")
            return {
                "verification": VerificationResult(
                    status=VerificationStatus.ERROR,
                    file_name=file_name,
                    blockchain_cid=blockchain_cid,
                    cids_match=False,
                    message=f"File exists on blockchain but could not be fetched from IPFS: {str(e)}"
                ),
                "file_bytes": None,
                "content_type": None
            }

        logger.info("Step 5: Computing SHA-256 checksum...")
        file_sha256 = compute_sha256(file_bytes)
        logger.info(f"  SHA-256: {file_sha256}")

        logger.info("Step 6: Verifying CID integrity...")
        on_chain_valid = await self.blockchain.verify_file(file_name, blockchain_cid)

        if on_chain_valid:
            verification = VerificationResult(
                status=VerificationStatus.VERIFIED,
                file_name=file_name,
                blockchain_cid=blockchain_cid,
                computed_cid=blockchain_cid,
                cids_match=True,
                timestamp=str(record["timestamp"]),
                registered_by=record["registered_by"],
                message=(
                    f"✅ INTEGRITY VERIFIED. File '{file_name}' is authentic. "
                    f"Content matches blockchain record. "
                    f"SHA-256: {file_sha256}"
                )
            )
            logger.info("  ✅ VERIFICATION PASSED")
        else:
            verification = VerificationResult(
                status=VerificationStatus.TAMPERED,
                file_name=file_name,
                blockchain_cid=blockchain_cid,
                cids_match=False,
                message=(
                    f"⚠️ INTEGRITY CHECK FAILED. "
                    f"On-chain verification returned false for '{file_name}'. "
                    f"The file may have been tampered with."
                )
            )
            logger.warning("  ⚠️ VERIFICATION FAILED — POSSIBLE TAMPERING")

        logger.info(f"=== VERIFICATION COMPLETE: {file_name} ===")

        return {
            "verification": verification,
            "file_bytes": file_bytes if on_chain_valid else None,
            "content_type": content_type if on_chain_valid else None
        }

    async def verify_only(self, file_name: str, provided_cid: str) -> VerificationResult:
        """Verify a CID against the blockchain record WITHOUT fetching the file."""
        exists = await self.blockchain.file_exists(file_name)
        if not exists:
            return VerificationResult(
                status=VerificationStatus.NOT_FOUND,
                file_name=file_name,
                cids_match=False,
                message=f"File '{file_name}' not found in registry"
            )

        blockchain_cid = await self.blockchain.get_file_cid(file_name)
        is_valid = verify_cid_match(blockchain_cid, provided_cid)

        if is_valid:
            return VerificationResult(
                status=VerificationStatus.VERIFIED,
                file_name=file_name,
                blockchain_cid=blockchain_cid,
                computed_cid=provided_cid,
                cids_match=True,
                message="✅ CID matches blockchain record. File is authentic."
            )
        else:
            return VerificationResult(
                status=VerificationStatus.TAMPERED,
                file_name=file_name,
                blockchain_cid=blockchain_cid,
                computed_cid=provided_cid,
                cids_match=False,
                message=(
                    f"⚠️ CID MISMATCH. "
                    f"Expected: {blockchain_cid}, "
                    f"Got: {provided_cid}. "
                    f"FILE HAS BEEN TAMPERED WITH."
                )
            )
