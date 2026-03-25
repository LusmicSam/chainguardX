"""
Service layer for interacting with the FileRegistry smart contract.
"""

import json
import logging
from pathlib import Path
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from app.config import get_settings

logger = logging.getLogger(__name__)


class BlockchainService:
    """Handles all smart contract interactions."""

    def __init__(self):
        settings = get_settings()

        self.w3 = Web3(Web3.HTTPProvider(settings.blockchain_rpc_url))
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        abi_path = Path(__file__).parent.parent.parent / "contract_abi" / "FileRegistry.json"
        with open(abi_path) as f:
            contract_json = json.load(f)
            abi = contract_json["abi"] if "abi" in contract_json else contract_json

        self.contract_address = Web3.to_checksum_address(settings.contract_address)
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=abi
        )

        self.private_key = settings.wallet_private_key
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.wallet_address = self.account.address

        logger.info(f"Blockchain service initialized")
        logger.info(f"  Contract: {self.contract_address}")
        logger.info(f"  Wallet: {self.wallet_address}")
        logger.info(f"  Connected: {self.w3.is_connected()}")

    def is_connected(self) -> bool:
        """Check if connected to the Ethereum node."""
        return self.w3.is_connected()

    async def register_file(
        self,
        file_name: str,
        cid: str,
        file_type: str,
        file_size: int
    ) -> dict:
        """Register a file on the blockchain."""
        logger.info(f"Registering file on blockchain: {file_name} → {cid}")

        try:
            nonce = self.w3.eth.get_transaction_count(self.wallet_address)

            transaction = self.contract.functions.registerFile(
                file_name, cid, file_type, file_size
            ).build_transaction({
                "from": self.wallet_address,
                "nonce": nonce,
                "gas": 500000,
                "gasPrice": self.w3.eth.gas_price,
                "chainId": get_settings().chain_id,
            })

            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )

            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            logger.info(f"Transaction sent: {tx_hash.hex()}")

            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if receipt["status"] != 1:
                raise Exception(
                    f"Transaction failed on-chain. Hash: {tx_hash.hex()}"
                )

            result = {
                "transaction_hash": tx_hash.hex(),
                "block_number": receipt["blockNumber"],
                "gas_used": receipt["gasUsed"],
                "status": "confirmed"
            }

            logger.info(
                f"✅ File registered on-chain. "
                f"Block: {receipt['blockNumber']}, "
                f"Gas used: {receipt['gasUsed']}"
            )
            return result

        except Exception as e:
            logger.error(f"Blockchain registration failed: {e}")
            raise

    async def get_file_cid(self, file_name: str) -> str:
        """Query the blockchain for a file's CID."""
        try:
            cid = self.contract.functions.getFileCID(file_name).call()
            logger.info(f"Blockchain CID for '{file_name}': {cid}")
            return cid
        except Exception as e:
            logger.error(f"Failed to get CID from blockchain: {e}")
            raise

    async def get_file_record(self, file_name: str) -> dict:
        """Get the complete file record from blockchain."""
        try:
            record = self.contract.functions.getFileRecord(file_name).call()
            return {
                "cid": record[0],
                "timestamp": record[1],
                "registered_by": record[2],
                "file_type": record[3],
                "file_size": record[4],
                "exists": record[5]
            }
        except Exception as e:
            logger.error(f"Failed to get file record: {e}")
            raise

    async def verify_file(self, file_name: str, cid: str) -> bool:
        """Call the smart contract's verifyFile function."""
        try:
            is_valid = self.contract.functions.verifyFile(file_name, cid).call()
            logger.info(f"Verification result for '{file_name}': {is_valid}")
            return is_valid
        except Exception as e:
            logger.error(f"Verification call failed: {e}")
            return False

    async def file_exists(self, file_name: str) -> bool:
        """Check if a file is registered on the blockchain."""
        try:
            return self.contract.functions.fileExists(file_name).call()
        except Exception as e:
            logger.error(f"File exists check failed: {e}")
            return False

    async def get_all_file_names(self) -> list:
        """Get all registered file names from the blockchain."""
        try:
            return self.contract.functions.getAllFileNames().call()
        except Exception as e:
            logger.error(f"Failed to get all file names: {e}")
            return []

    async def get_file_history(self, file_name: str) -> list:
        """Get all historical CIDs for a file."""
        try:
            return self.contract.functions.getFileHistory(file_name).call()
        except Exception as e:
            logger.error(f"Failed to get file history: {e}")
            return []

    async def get_total_files(self) -> int:
        """Get total number of registered files."""
        try:
            return self.contract.functions.totalFiles().call()
        except Exception as e:
            logger.error(f"Failed to get total files: {e}")
            return 0
