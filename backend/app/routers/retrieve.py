"""
Retrieval endpoint: Fetches file from IPFS, verifies against blockchain, serves to client.
"""

import logging
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response, JSONResponse
from app.models.schemas import (
    FileRetrieveResponse,
    VerificationResult,
    VerificationStatus,
    ErrorResponse
)
from app.services.pinata_service import PinataService
from app.services.blockchain_service import BlockchainService
from app.services.verification_service import VerificationService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Retrieve & Verify"])


@router.get(
    "/file/{file_name}",
    summary="Retrieve and verify a file",
    responses={
        200: {"description": "File served with verification headers"},
        404: {"model": ErrorResponse, "description": "File not registered"},
        409: {"model": ErrorResponse, "description": "Integrity check failed"}
    }
)
async def retrieve_file(file_name: str):
    """Retrieve a file with blockchain-verified integrity."""
    logger.info(f"Retrieve request for: {file_name}")

    try:
        pinata = PinataService()
        blockchain = BlockchainService()
        verifier = VerificationService(pinata, blockchain)

        result = await verifier.verify_and_fetch(file_name)
        verification = result["verification"]

        if verification.status == VerificationStatus.NOT_FOUND:
            raise HTTPException(
                status_code=404,
                detail=verification.message
            )

        if verification.status == VerificationStatus.TAMPERED:
            raise HTTPException(
                status_code=409,
                detail=verification.message
            )

        if verification.status == VerificationStatus.ERROR:
            raise HTTPException(
                status_code=502,
                detail=verification.message
            )

        if verification.status == VerificationStatus.VERIFIED:
            file_bytes = result["file_bytes"]
            content_type = result["content_type"]

            response = Response(
                content=file_bytes,
                media_type=content_type,
                headers={
                    "X-ChainGuard-Status": "verified",
                    "X-ChainGuard-CID": verification.blockchain_cid,
                    "X-ChainGuard-Blockchain-Verified": "true",
                    "X-ChainGuard-File-Name": file_name,
                    "X-ChainGuard-Registered-By": verification.registered_by or "",
                    "X-ChainGuard-Timestamp": verification.timestamp or "",
                    "Content-Disposition": f'inline; filename="{file_name}"',
                    "Cache-Control": "public, max-age=3600",
                }
            )
            return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Retrieve error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/verify/{file_name}",
    response_model=VerificationResult,
    summary="Verify a file's integrity without downloading",
)
async def verify_file(file_name: str):
    """Verify file integrity without downloading the file content."""
    try:
        blockchain = BlockchainService()

        exists = await blockchain.file_exists(file_name)
        if not exists:
            return VerificationResult(
                status=VerificationStatus.NOT_FOUND,
                file_name=file_name,
                cids_match=False,
                message=f"File '{file_name}' is not registered"
            )

        record = await blockchain.get_file_record(file_name)
        blockchain_cid = record["cid"]

        return VerificationResult(
            status=VerificationStatus.VERIFIED,
            file_name=file_name,
            blockchain_cid=blockchain_cid,
            cids_match=True,
            timestamp=str(record["timestamp"]),
            registered_by=record["registered_by"],
            message=f"✅ File '{file_name}' is registered on blockchain with CID: {blockchain_cid}"
        )

    except Exception as e:
        logger.error(f"Verification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/verify-cid",
    response_model=VerificationResult,
    summary="Verify a specific CID against blockchain record",
)
async def verify_cid(
    file_name: str = Query(..., description="Registered file name"),
    cid: str = Query(..., description="CID to verify")
):
    """Verify a provided CID against the blockchain record."""
    try:
        pinata = PinataService()
        blockchain = BlockchainService()
        verifier = VerificationService(pinata, blockchain)

        result = await verifier.verify_only(file_name, cid)
        return result

    except Exception as e:
        logger.error(f"CID verification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
