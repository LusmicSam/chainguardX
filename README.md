# ChainGuard — Blockchain-Verified File Integrity System

A decentralized system for uploading files to IPFS and verifying their integrity using Ethereum smart contracts.

## 🏗️ Architecture Overview

```
Browser/Client ↔ FastAPI Backend ↔ Pinata (IPFS) ↔ Ethereum Blockchain
                                  ↕
                            File Storage & 
                            CID Verification
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm 9+
- Git
- MetaMask browser extension

### Phase 1: Setup Smart Contract

```bash
cd contracts

# Install dependencies
npm install

# Compile contract
npx hardhat compile

# Run tests
npx hardhat test

# Deploy to Sepolia testnet
npx hardhat run scripts/deploy.js --network sepolia

# Copy ABI to backend
cp artifacts/contracts/FileRegistry.sol/FileRegistry.json ../backend/contract_abi/
```

### Phase 2: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Edit .env with your values:
# - PINATA_API_KEY, PINATA_SECRET_KEY, PINATA_JWT
# - CONTRACT_ADDRESS (from Phase 1)
# - BLOCKCHAIN_RPC_URL (Alchemy/Infura)
# - WALLET_PRIVATE_KEY
# - CHAIN_ID=11155111 (Sepolia)

# Run backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# API docs: http://localhost:8000/docs
```

### Phase 3: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:5173
```

## 📋 Configuration

### Backend .env

```env
# Pinata Configuration
PINATA_API_KEY=your_pinata_api_key
PINATA_SECRET_KEY=your_pinata_secret_key
PINATA_JWT=your_pinata_jwt_token
PINATA_GATEWAY_URL=https://gateway.pinata.cloud/ipfs/

# Blockchain Configuration
CONTRACT_ADDRESS=0xYourDeployedContractAddress
BLOCKCHAIN_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
WALLET_PRIVATE_KEY=your_wallet_private_key
CHAIN_ID=11155111

# Application
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=.png,.jpg,.jpeg,.gif,.pdf,.json,.csv,.txt,.doc,.docx
```

## 🔑 API Endpoints

### Upload & Register File
```http
POST /api/v1/upload
Content-Type: multipart/form-data

file: <binary file data>
```

**Response:**
```json
{
  "success": true,
  "file_name": "document.pdf",
  "ipfs_cid": "QmX...",
  "ipfs_url": "https://gateway.pinata.cloud/ipfs/QmX...",
  "file_size": 1024,
  "file_type": "application/pdf",
  "transaction_hash": "0xabc123...",
  "block_number": 5678901,
  "message": "File successfully uploaded..."
}
```

### Retrieve & Verify File
```http
GET /api/v1/file/{file_name}
```

**Response:** File binary data with verification headers

**Headers:**
- `X-ChainGuard-Status`: verified/tampered/not_found
- `X-ChainGuard-CID`: IPFS Content Identifier
- `X-ChainGuard-Blockchain-Verified`: true/false
- `X-ChainGuard-Registered-By`: Wallet address
- `X-ChainGuard-Timestamp`: Registration timestamp

### Verify Without Download
```http
GET /api/v1/verify/{file_name}
```

### List Registry
```http
GET /api/v1/registry
```

### System Health
```http
GET /api/v1/health
```

## 🔐 Security Model

1. **IPFS Content Addressing**: Files are stored by their SHA-256 hash (CID)
   - Any modification to file content changes its CID
   - Impossible for attacker to serve modified content under the same CID

2. **Blockchain Immutability**: File CID is registered on-chain
   - Ethereum blockchain is immutable
   - CID cannot be changed after registration
   - Only owner can register new files

3. **Verification Flow**:
   ```
   1. Backend queries blockchain for trusted CID
   2. Backend fetches file from IPFS using that CID
   3. Backend verifies on-chain that CID matches
   4. If CIDs match → file is authentic
   5. If CIDs don't match → file has been tampered with
   ```

## 🧪 Testing

### Smart Contract Tests
```bash
cd contracts
npx hardhat test
```

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

## 📦 Deployment

### Docker Deployment
```bash
# Build and run with docker-compose
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### Production Deployment

#### Backend (Railway/Render)
```bash
# Set environment variables in deployment platform
# Deploy the backend directory

# Environment variables needed:
PINATA_API_KEY=...
BLOCKCHAIN_RPC_URL=...
CONTRACT_ADDRESS=...
WALLET_PRIVATE_KEY=...
```

#### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy the `dist` directory
```

## 📚 Project Structure

```
chainguard/
├── contracts/                    # Smart contracts
│   ├── contracts/FileRegistry.sol
│   ├── scripts/deploy.js
│   ├── test/FileRegistry.test.js
│   └── hardhat.config.js
│
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── models/              # Pydantic schemas
│   │   └── utils/               # Utilities
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
│
├── frontend/                     # React app
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── services/api.js
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── scripts/                      # Utilities
│   └── verify_client.py          # Client-side verification
│
└── docker-compose.yml
```

## 🛠️ Development Workflow

1. **Start Hardhat local node** (optional, for local development):
   ```bash
   cd contracts
   npx hardhat node
   ```

2. **Deploy contract** (to local node or testnet):
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   # or
   npx hardhat run scripts/deploy.js --network sepolia
   ```

3. **Copy contract ABI**:
   ```bash
   cp contracts/artifacts/contracts/FileRegistry.sol/FileRegistry.json backend/contract_abi/
   ```

4. **Update backend .env** with contract address

5. **Run backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

6. **Run frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🔍 Client-Side Verification

Use the standalone verification script to independently verify files:

```bash
python scripts/verify_client.py "document.pdf"
```

This script:
1. Fetches file from ChainGuard API
2. Independently queries the blockchain
3. Verifies CID matches on-chain record
4. Computes SHA-256 hash
5. Reports integrity status

## 📖 Key Technologies

- **Smart Contracts**: Solidity 0.8.19, Hardhat
- **Blockchain**: Ethereum Sepolia Testnet
- **File Storage**: IPFS (via Pinata)
- **Backend**: Python FastAPI, web3.py
- **Frontend**: React 18, Vite, Axios
- **Node Provider**: Alchemy or Infura
- **Docker**: Container orchestration

## 🚨 Important Notes

1. **Private Keys**: Never commit `.env` files with real private keys
2. **Gas Costs**: Each file registration costs gas on the blockchain
3. **IPFS Pinning**: Files are pinned on Pinata for reliability
4. **Rate Limiting**: Add rate limiting in production
5. **Authentication**: Add API key authentication in production

## 📝 License

MIT

## 🤝 Support

For issues or questions, please create an issue in the repository.

---

**ChainGuard**: Bringing immutable integrity verification to decentralized file storage.
