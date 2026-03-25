"""
Service layer for interacting with Pinata's IPFS pinning API.
"""

import httpx
import logging
from typing import Optional, Tuple
from app.config import get_settings

logger = logging.getLogger(__name__)


class PinataService:
    """Handles all interactions with Pinata IPFS service."""

    BASE_URL = "https://api.pinata.cloud"

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.pinata_api_key
        self.secret_key = settings.pinata_secret_key
        self.jwt = settings.pinata_jwt
        self.gateway_url = settings.pinata_gateway_url

        self.headers = {
            "Authorization": f"Bearer {self.jwt}"
        }

    async def test_connection(self) -> bool:
        """Test Pinata API connectivity."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/data/testAuthentication",
                    headers=self.headers,
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Pinata connection test failed: {e}")
            return False

    async def upload_file(
        self,
        file_bytes: bytes,
        file_name: str,
        file_type: str
    ) -> Tuple[str, int]:
        """Upload a file to IPFS via Pinata."""
        logger.info(f"Uploading file '{file_name}' to Pinata ({len(file_bytes)} bytes)")

        import json
        pinata_metadata = json.dumps({
            "name": file_name,
            "keyvalues": {
                "source": "chainguard",
                "fileType": file_type
            }
        })

        pinata_options = json.dumps({
            "cidVersion": 0
        })

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                files = {
                    "file": (file_name, file_bytes, file_type)
                }
                data = {
                    "pinataMetadata": pinata_metadata,
                    "pinataOptions": pinata_options
                }

                response = await client.post(
                    f"{self.BASE_URL}/pinning/pinFileToIPFS",
                    headers=self.headers,
                    files=files,
                    data=data
                )

                if response.status_code != 200:
                    error_detail = response.text
                    logger.error(f"Pinata upload failed: {response.status_code} - {error_detail}")
                    raise Exception(f"Pinata upload failed: {error_detail}")

                result = response.json()
                cid = result["IpfsHash"]
                pin_size = result["PinSize"]

                logger.info(f"✅ File uploaded successfully. CID: {cid}")
                return cid, pin_size

        except httpx.TimeoutException:
            logger.error("Pinata upload timed out")
            raise Exception("Upload to IPFS timed out. Try a smaller file.")
        except Exception as e:
            logger.error(f"Pinata upload error: {e}")
            raise

    async def fetch_file(self, cid: str) -> Tuple[bytes, str]:
        """Fetch a file from IPFS via Pinata's gateway."""
        url = f"{self.gateway_url}{cid}"
        logger.info(f"Fetching file from IPFS: {url}")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(url)

                if response.status_code == 404:
                    raise Exception(f"File not found on IPFS: {cid}")

                if response.status_code != 200:
                    raise Exception(
                        f"IPFS fetch failed: {response.status_code} - {response.text}"
                    )

                content_type = response.headers.get("content-type", "application/octet-stream")
                file_bytes = response.content

                logger.info(
                    f"✅ File fetched: {len(file_bytes)} bytes, type: {content_type}"
                )
                return file_bytes, content_type

        except httpx.TimeoutException:
            logger.error(f"IPFS fetch timed out for CID: {cid}")
            raise Exception("Fetching from IPFS timed out")
        except Exception as e:
            logger.error(f"IPFS fetch error: {e}")
            raise

    async def unpin_file(self, cid: str) -> bool:
        """Unpin a file from Pinata (remove from IPFS pinning)."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(
                    f"{self.BASE_URL}/pinning/unpin/{cid}",
                    headers=self.headers
                )
                success = response.status_code == 200
                if success:
                    logger.info(f"✅ File unpinned: {cid}")
                else:
                    logger.warning(f"Unpin failed for {cid}: {response.text}")
                return success
        except Exception as e:
            logger.error(f"Unpin error: {e}")
            return False

    async def list_pins(self, limit: int = 100) -> list:
        """List all pinned files on Pinata."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/data/pinList?pageLimit={limit}&status=pinned",
                    headers=self.headers
                )
                if response.status_code == 200:
                    return response.json().get("rows", [])
                return []
        except Exception as e:
            logger.error(f"List pins error: {e}")
            return []

    def get_gateway_url(self, cid: str) -> str:
        """Construct the public gateway URL for a CID."""
        return f"{self.gateway_url}{cid}"
