"""
Registry endpoints: List files, get history, health check.
"""

import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    RegistryListResponse,
    FileRecord,
    FileHistoryResponse,
    HealthResponse,
    ErrorResponse
)
from app.services.pinata_service import PinataService
from app.services.blockchain_service import BlockchainService
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Registry"])


@router.get(
    "/registry",
    response_model=RegistryListResponse,
    summary="List all registered files",
)
async def list_files():
    """List all files in the blockchain registry."""
    try:
        blockchain = BlockchainService()
        file_names = await blockchain.get_all_file_names()
        total = await blockchain.get_total_files()

        files = []
        for name in file_names:
            try:
                record = await blockchain.get_file_record(name)
                files.append(FileRecord(
                    file_name=name,
                    cid=record["cid"],
                    file_type=record["file_type"],
                    file_size=record["file_size"],
                    timestamp=str(record["timestamp"]),
                    registered_by=record["registered_by"]
                ))
            except Exception as e:
                logger.warning(f"Failed to get record for '{name}': {e}")

        return RegistryListResponse(total_files=total, files=files)

    except Exception as e:
        logger.error(f"Registry list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/registry/{file_name}/history",
    response_model=FileHistoryResponse,
    summary="Get file version history",
)
async def file_history(file_name: str):
    """Get the version history of a registered file."""
    try:
        blockchain = BlockchainService()
        exists = await blockchain.file_exists(file_name)

        if not exists:
            raise HTTPException(
                status_code=404,
                detail=f"File '{file_name}' not found"
            )

        history = await blockchain.get_file_history(file_name)
        return FileHistoryResponse(
            file_name=file_name,
            versions=history,
            total_versions=len(history)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"History error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System health check",
)
async def health_check():
    """Check system health: Pinata + Blockchain connectivity."""
    settings = get_settings()

    pinata_ok = False
    blockchain_ok = False

    try:
        pinata = PinataService()
        pinata_ok = await pinata.test_connection()
    except Exception as e:
        logger.warning(f"Pinata health check failed: {e}")

    try:
        blockchain = BlockchainService()
        blockchain_ok = blockchain.is_connected()
    except Exception as e:
        logger.warning(f"Blockchain health check failed: {e}")

    status = "healthy" if (pinata_ok and blockchain_ok) else "degraded"

    return HealthResponse(
        status=status,
        pinata_connected=pinata_ok,
        blockchain_connected=blockchain_ok,
        contract_address=settings.contract_address,
        network=f"chain_id_{settings.chain_id}",
        timestamp=datetime.now(timezone.utc).isoformat()
    )
