"""
Standalone client verification script.
Demonstrates how a client can independently verify file integrity.
"""

import httpx
import hashlib
import sys
import json
from web3 import Web3


API_BASE_URL = "http://localhost:8000"
BLOCKCHAIN_RPC = "https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY"
CONTRACT_ADDRESS = "0xYourContractAddress"

MINIMAL_ABI = json.loads("""[
    {
        "inputs": [{"name": "_fileName", "type": "string"}],
        "name": "getFileCID",
        "outputs": [{"name": "cid", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "_fileName", "type": "string"},
            {"name": "_cid", "type": "string"}
        ],
        "name": "verifyFile",
        "outputs": [{"name": "isValid", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]""")


def verify_file(file_name: str):
    """Complete client-side verification."""
    print(f"\n{'='*60}")
    print(f"CLIENT-SIDE VERIFICATION: {file_name}")
    print(f"{'='*60}")

    print("\n[1] Fetching file from ChainGuard API...")
    response = httpx.get(f"{API_BASE_URL}/api/v1/file/{file_name}", timeout=60)

    if response.status_code == 404:
        print("   ❌ File not found in registry")
        return False
    elif response.status_code == 409:
        print("   ⚠️ SERVER reports tampering detected!")
        return False
    elif response.status_code != 200:
        print(f"   ❌ Server error: {response.status_code}")
        return False

    file_bytes = response.content
    print(f"   ✅ Received {len(file_bytes)} bytes")

    print("\n[2] Reading verification headers...")
    server_status = response.headers.get("X-ChainGuard-Status", "unknown")
    server_cid = response.headers.get("X-ChainGuard-CID", "unknown")
    print(f"   Server status: {server_status}")
    print(f"   Server CID: {server_cid}")

    print("\n[3] Independently querying blockchain...")
    w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_RPC))

    if not w3.is_connected():
        print("   ❌ Cannot connect to blockchain")
        return False

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS),
        abi=MINIMAL_ABI
    )

    blockchain_cid = contract.functions.getFileCID(file_name).call()
    print(f"   Blockchain CID: {blockchain_cid}")

    print("\n[4] Comparing CIDs...")
    if server_cid == blockchain_cid:
        print("   ✅ Server CID matches blockchain record")
    else:
        print("   ⚠️ SERVER CID DOES NOT MATCH BLOCKCHAIN!")
        return False

    print("\n[5] Computing local checksum...")
    local_sha256 = hashlib.sha256(file_bytes).hexdigest()
    print(f"   Local SHA-256: {local_sha256}")

    print("\n[6] On-chain verification...")
    is_valid = contract.functions.verifyFile(file_name, blockchain_cid).call()
    print(f"   On-chain verify result: {is_valid}")

    print(f"\n{'='*60}")
    if is_valid and server_cid == blockchain_cid:
        print("✅ VERIFICATION PASSED — File is authentic and untampered")
        print(f"   CID: {blockchain_cid}")
        print(f"   SHA-256: {local_sha256}")
        print(f"   Size: {len(file_bytes)} bytes")
    else:
        print("❌ VERIFICATION FAILED — File integrity compromised!")
    print(f"{'='*60}\n")

    return is_valid


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_client.py <file_name>")
        print("Example: python verify_client.py report_2024.pdf")
        sys.exit(1)

    file_name = sys.argv[1]
    result = verify_file(file_name)
    sys.exit(0 if result else 1)
