"""
Utility functions for computing and verifying IPFS CID hashes.
"""

import hashlib
import base58
import struct


def compute_sha256(file_bytes: bytes) -> str:
    """Compute SHA-256 hash of file bytes."""
    return hashlib.sha256(file_bytes).hexdigest()


def compute_ipfs_cid_v0(file_bytes: bytes) -> str:
    """
    Compute IPFS CID v0 for small files (< 256KB).
    WARNING: This only works correctly for files that fit in a single IPFS block.
    """
    sha256_hash = hashlib.sha256(file_bytes).digest()
    multihash = bytes([0x12, 0x20]) + sha256_hash
    return base58.b58encode(multihash).decode('utf-8')


def verify_cid_match(blockchain_cid: str, fetched_cid: str) -> bool:
    """
    Compare two CID strings for equality.
    Returns True if CIDs match (file is authentic).
    """
    return blockchain_cid.strip() == fetched_cid.strip()


def compute_file_checksum(file_bytes: bytes) -> dict:
    """Compute multiple checksums for a file."""
    return {
        "sha256": hashlib.sha256(file_bytes).hexdigest(),
        "md5": hashlib.md5(file_bytes).hexdigest(),
        "sha1": hashlib.sha1(file_bytes).hexdigest(),
        "size_bytes": len(file_bytes),
    }
