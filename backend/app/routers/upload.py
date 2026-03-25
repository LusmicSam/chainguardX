"""
Upload endpoint: Receives file → Pins to IPFS → Registers on blockchain.
"""

import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.config import get_settings, Settings
from app.models.schemas import FileUploadResponse, ErrorResponse
from app.services.pinata_service import PinataService
from app.services.blockchain_service import BlockchainService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Upload"])


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Upload file to IPFS and register on blockchain",
)
async def upload_file(
    file: UploadFile = File(..., description="The file to upload and register"),
    settings: Settings = Depends(get_settings)
):
    """Upload a file to IPFS and register its CID on the blockchain."""
    logger.info(f"Upload request received: {file.filename}")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_ext}' not allowed. "
                   f"Allowed: {settings.allowed_extensions_list}"
        )

    file_bytes = await file.read()
    file_size = len(file_bytes)

    if file_size > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({file_size} bytes). "
                   f"Maximum: {settings.max_file_size_mb} MB"
        )

    if file_size == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    file_type = file.content_type or "application/octet-stream"
    file_name = file.filename

    try:
        logger.info("Step 1: Uploading to IPFS via Pinata...")
        pinata = PinataService()
        cid, pin_size = await pinata.upload_file(file_bytes, file_name, file_type)
        ipfs_url = pinata.get_gateway_url(cid)
        logger.info(f"  IPFS CID: {cid}")
        logger.info(f"  IPFS URL: {ipfs_url}")

        logger.info("Step 2: Registering on blockchain...")
        blockchain = BlockchainService()
        tx_result = await blockchain.register_file(
            file_name=file_name,
            cid=cid,
            file_type=file_type,
            file_size=file_size
        )
        logger.info(f"  TX Hash: {tx_result['transaction_hash']}")
        logger.info(f"  Block: {tx_result['block_number']}")

        return FileUploadResponse(
            success=True,
            file_name=file_name,
            ipfs_cid=cid,
            ipfs_url=ipfs_url,
            file_size=file_size,
            file_type=file_type,
            transaction_hash=tx_result["transaction_hash"],
            block_number=tx_result["block_number"],
            message=(
                f"File '{file_name}' successfully uploaded to IPFS "
                f"and registered on blockchain. "
                f"CID: {cid}"
            )
        )

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
