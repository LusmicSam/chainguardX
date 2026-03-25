"""
ChainGuard API — Blockchain-Verified File Integrity System
Entry point for the FastAPI application.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, retrieve, registry
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ChainGuard API",
    description="""
    ## Blockchain-Verified File Integrity System

    ChainGuard uses IPFS (via Pinata) for decentralized file storage
    and Ethereum smart contracts for immutable integrity verification.

    ### Architecture:
    - **Storage**: Files are stored on IPFS via Pinata
    - **Ledger**: File CIDs are registered on Ethereum blockchain
    - **Verification**: Every file retrieval is verified against the blockchain

    ### Endpoints:
    - `POST /api/v1/upload` — Upload and register a file
    - `GET /api/v1/file/{name}` — Retrieve with verification
    - `GET /api/v1/verify/{name}` — Check integrity without download
    - `GET /api/v1/registry` — List all registered files
    - `GET /api/v1/health` — System health check
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "X-ChainGuard-Status",
        "X-ChainGuard-CID",
        "X-ChainGuard-Blockchain-Verified",
        "X-ChainGuard-File-Name",
        "X-ChainGuard-Registered-By",
        "X-ChainGuard-Timestamp",
    ]
)

app.include_router(upload.router)
app.include_router(retrieve.router)
app.include_router(registry.router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    settings = get_settings()
    logger.info("=" * 60)
    logger.info("ChainGuard API Starting...")
    logger.info(f"  Contract: {settings.contract_address}")
    logger.info(f"  Chain ID: {settings.chain_id}")
    logger.info(f"  Debug: {settings.debug}")
    logger.info("=" * 60)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint — API information."""
    return {
        "name": "ChainGuard API",
        "version": "1.0.0",
        "description": "Blockchain-Verified File Integrity System",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
