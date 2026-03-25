"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """All configuration is loaded from .env file or environment variables."""

    pinata_api_key: str
    pinata_secret_key: str
    pinata_jwt: str
    pinata_gateway_url: str = "https://gateway.pinata.cloud/ipfs/"

    contract_address: str
    blockchain_rpc_url: str
    wallet_private_key: str
    chain_id: int = 11155111

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False
    max_file_size_mb: int = 50
    allowed_extensions: str = ".png,.jpg,.jpeg,.gif,.pdf,.json,.csv,.txt"

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [ext.strip() for ext in self.allowed_extensions.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance - loaded once."""
    return Settings()
