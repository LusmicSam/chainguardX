"""
Request/Response schemas for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class VerificationStatus(str, Enum):
    """Possible verification outcomes."""
    VERIFIED = "verified"
    TAMPERED = "tampered"
    NOT_FOUND = "not_found"
    ERROR = "verification_error"


class FileUploadResponse(BaseModel):
    """Response after successful file upload."""
    success: bool
    file_name: str
    ipfs_cid: str
    ipfs_url: str
    file_size: int
    file_type: str
    transaction_hash: str
    block_number: int
    message: str


class FileRetrieveRequest(BaseModel):
    """Request to retrieve and verify a file."""
    file_name: str = Field(..., description="The registered file name to retrieve")


class VerificationResult(BaseModel):
    """Detailed verification result."""
    status: VerificationStatus
    file_name: str
    blockchain_cid: Optional[str] = None
    computed_cid: Optional[str] = None
    cids_match: bool = False
    timestamp: Optional[str] = None
    registered_by: Optional[str] = None
    message: str


class FileRetrieveResponse(BaseModel):
    """Response when retrieving a verified file."""
    success: bool
    file_name: str
    verification: VerificationResult
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    served_from: str = "ipfs_via_pinata"


class FileRecord(BaseModel):
    """Single file record from the registry."""
    file_name: str
    cid: str
    file_type: str
    file_size: int
    timestamp: str
    registered_by: str


class RegistryListResponse(BaseModel):
    """Response listing all registered files."""
    total_files: int
    files: List[FileRecord]


class FileHistoryResponse(BaseModel):
    """Version history for a file."""
    file_name: str
    versions: List[str]
    total_versions: int


class HealthResponse(BaseModel):
    """System health check response."""
    status: str
    pinata_connected: bool
    blockchain_connected: bool
    contract_address: str
    network: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None
