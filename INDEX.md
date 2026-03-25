# ChainGuard - Project Index

Welcome to ChainGuard! This is a blockchain-verified file integrity system. Here's how to navigate the project.

## 📚 Documentation (Start Here!)

### 1. **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** ⭐ START HERE
   - Overview of what was built
   - Complete file structure
   - Quick start guide (5 steps)
   - Technologies used
   - Deployment checklist

### 2. **[README.md](./README.md)**
   - Project description
   - Architecture diagram
   - API endpoints reference
   - Security model explanation
   - Project structure details

### 3. **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** 📖 STEP-BY-STEP
   - Get API keys (Pinata, Alchemy)
   - Phase 1: Deploy smart contract
   - Phase 2: Setup backend
   - Phase 3: Setup frontend
   - End-to-end testing
   - Troubleshooting common issues

### 4. **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** ✅ BEFORE GOING LIVE
   - Pre-deployment setup
   - Phase-by-phase verification
   - Production deployment options
   - Security checklist
   - Monitoring and maintenance

---

## 🏗️ Project Structure

```
chainguard/
├── contracts/              # Solidity Smart Contracts
│   ├── contracts/
│   │   └── FileRegistry.sol       (145 lines - main contract)
│   ├── test/
│   │   └── FileRegistry.test.js   (smart contract tests)
│   ├── scripts/
│   │   └── deploy.js              (deployment script)
│   ├── hardhat.config.js
│   ├── package.json
│   └── .env                       (create with your API keys)
│
├── backend/                # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py               (FastAPI app entry point)
│   │   ├── config.py             (configuration management)
│   │   ├── models/
│   │   │   └── schemas.py        (API request/response models)
│   │   ├── services/
│   │   │   ├── pinata_service.py       (IPFS management)
│   │   │   ├── blockchain_service.py   (smart contract calls)
│   │   │   └── verification_service.py (integrity verification)
│   │   ├── routers/
│   │   │   ├── upload.py         (file upload endpoint)
│   │   │   ├── retrieve.py       (file retrieval endpoint)
│   │   │   └── registry.py       (registry & health endpoints)
│   │   └── utils/
│   │       └── hashing.py        (hash computation utilities)
│   ├── tests/                    (pytest test cases)
│   ├── requirements.txt          (Python dependencies)
│   ├── .env                      (create with your configuration)
│   └── Dockerfile               (for containerization)
│
├── frontend/               # React + Vite Dashboard
│   ├── src/
│   │   ├── App.jsx               (main dashboard component)
│   │   ├── main.jsx              (React entry point)
│   │   ├── index.css             (global styles)
│   │   ├── components/
│   │   │   ├── FileUpload.jsx    (upload form component)
│   │   │   ├── FileList.jsx      (file registry display)
│   │   │   ├── FileRetrieval.jsx (download component)
│   │   │   └── VerificationBadge.jsx (status indicator)
│   │   └── services/
│   │       └── api.js            (API communication)
│   ├── index.html               (HTML entry point)
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile               (for containerization)
│
├── scripts/                # Utility Scripts
│   └── verify_client.py         (standalone file verification)
│
├── docker-compose.yml          (run all services together)
├── .gitignore
├── README.md                   (project overview)
├── SETUP_GUIDE.md             (installation instructions)
├── DEPLOYMENT_CHECKLIST.md    (pre-deployment tasks)
├── PROJECT_SUMMARY.md         (what was built)
└── INDEX.md                   (this file)
```

---

## 🚀 Quick Start (5 Steps)

```bash
# Step 1: Deploy Contract
cd contracts
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
# Save the contract address!

# Step 2: Copy ABI
cp artifacts/contracts/FileRegistry.sol/FileRegistry.json ../backend/contract_abi/

# Step 3: Run Backend
cd ../backend
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Edit .env with your API keys
uvicorn app.main:app --reload

# Step 4: Run Frontend (in another terminal)
cd frontend
npm install
npm run dev

# Step 5: Open http://localhost:5173 🎉
```

---

## 📖 Component Documentation

### Smart Contract: `contracts/contracts/FileRegistry.sol`
- **Purpose**: Immutable file registry on blockchain
- **Functions**: 
  - `registerFile()` - register a file CID
  - `getFileCID()` - retrieve file's CID
  - `verifyFile()` - verify CID authenticity
  - `getFileRecord()` - get complete file info
  - `getAllFileNames()` - list all files
  - `getFileHistory()` - get version history
- **Security**: Owner-only registration, CID uniqueness, version tracking

### Backend Services

#### `app/services/pinata_service.py`
- **Purpose**: IPFS file management via Pinata API
- **Methods**:
  - `upload_file()` - upload file to IPFS, get CID
  - `fetch_file()` - download file from IPFS
  - `unpin_file()` - remove file from Pinata
  - `test_connection()` - verify Pinata connectivity

#### `app/services/blockchain_service.py`
- **Purpose**: Smart contract interaction
- **Methods**:
  - `register_file()` - write file record to blockchain
  - `get_file_cid()` - read file's CID from blockchain
  - `verify_file()` - verify CID matches on-chain
  - `get_all_file_names()` - enumerate registered files

#### `app/services/verification_service.py`
- **Purpose**: Core integrity verification logic
- **Methods**:
  - `verify_and_fetch()` - fetch file + verify + return
  - `verify_only()` - verify without fetching

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/upload` | Upload file to IPFS + register on blockchain |
| GET | `/api/v1/file/{name}` | Retrieve verified file |
| GET | `/api/v1/verify/{name}` | Check integrity without downloading |
| POST | `/api/v1/verify-cid` | Verify specific CID |
| GET | `/api/v1/registry` | List all registered files |
| GET | `/api/v1/health` | System health check |

### Frontend Components

| Component | Purpose |
|-----------|---------|
| `App.jsx` | Main dashboard, tab navigation |
| `FileUpload.jsx` | Drag-drop file upload form |
| `FileList.jsx` | Display registry of all files |
| `FileRetrieval.jsx` | Download and verify files |
| `VerificationBadge.jsx` | Show verification status |

---

## 🔐 Security Architecture

```
User → Frontend (React)
       ↓
       Backend (FastAPI) ← Verifies integrity
       ↓       ↓
    IPFS    Blockchain (Ethereum)
    (Files  (CID Ledger -
     stored  immutable)
     by
     content
     hash)
```

**Key Security Features:**
- Content-addressed storage (IPFS): Files stored by SHA-256 hash
- Immutable ledger (Blockchain): CIDs recorded on-chain, can't be changed
- Verification: Downloaded file's CID compared to blockchain record
- Tampering Detection: Modified file = different CID = mismatch detected

---

## 📋 Typical Usage Flow

### 1. **User Uploads File**
```
User selects file
  ↓
Frontend uploads to Backend
  ↓
Backend uploads to Pinata (IPFS)
  ↓
Pinata returns CID
  ↓
Backend registers CID on Blockchain
  ↓
User sees: ✅ Upload successful, CID: Qm...
```

### 2. **User Wants to Retrieve File**
```
User requests file by name
  ↓
Backend queries Blockchain for CID
  ↓
Backend fetches file from IPFS using CID
  ↓
Backend verifies CID matches blockchain record
  ↓
If match: File served ✅ VERIFIED
If no match: Tampering alert ⚠️ TAMPERED
```

### 3. **Integrity Verified**
```
CID on blockchain = CID on IPFS → File is authentic ✅
CID on blockchain ≠ CID on IPFS → File was modified ⚠️
```

---

## 🧪 Testing

### Smart Contract Tests
```bash
cd contracts
npx hardhat test
```

### Backend Tests
```bash
cd backend
source venv/bin/activate  # activate venv
pytest tests/ -v
```

### Manual Testing
1. Upload a file via frontend
2. Verify it appears in Registry
3. Download and verify it's authentic
4. Check transaction on Etherscan

---

## 🐳 Docker Deployment

Run all components with one command:
```bash
docker-compose up --build
```

Services:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 🚀 Production Deployment

### Option 1: Individual Cloud Deployment
- **Backend**: Railway, Render, or AWS EC2
- **Frontend**: Vercel or Netlify
- See [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

### Option 2: Docker Deployment
- Push to Docker Hub
- Deploy on cloud platform (AWS, GCP, Azure)
- Use docker-compose for orchestration

### Option 3: Serverless
- Deploy backend on AWS Lambda/Google Cloud Functions
- Deploy frontend on CDN (Vercel/Netlify)

---

## 🔗 External Resources

### Setup Prerequisites
- **Get Testnet ETH**: https://sepoliafaucet.com/
- **Pinata**: https://app.pinata.cloud/
- **Alchemy**: https://www.alchemy.com/
- **Etherscan**: https://sepolia.etherscan.io/

### Smart Contract
- **Solidity Docs**: https://docs.soliditylang.org/
- **Hardhat**: https://hardhat.org/
- **OpenZeppelin**: https://docs.openzeppelin.com/

### Backend
- **FastAPI**: https://fastapi.tiangolo.com/
- **web3.py**: https://web3py.readthedocs.io/
- **Pydantic**: https://docs.pydantic.dev/

### Frontend
- **React**: https://react.dev/
- **Vite**: https://vitejs.dev/
- **Axios**: https://axios-http.com/

### Blockchain
- **Ethereum**: https://ethereum.org/
- **Sepolia Testnet**: https://sepolia.dev/
- **IPFS**: https://ipfs.io/

---

## 🆘 Common Issues

### Backend won't connect to blockchain
- Check `BLOCKCHAIN_RPC_URL` in .env
- Verify it's the Sepolia testnet URL
- Make sure it includes the API key

### Frontend can't reach backend
- Verify backend is running on port 8000
- Check `API_BASE` in `frontend/src/services/api.js`
- Look for CORS errors in browser console

### File upload fails
- Check Pinata JWT token is valid
- Verify file size < 50MB
- Check file extension is allowed

### Blockchain transaction fails
- Wallet needs ETH (get from faucet)
- Contract address must be correct
- Private key must be valid

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed troubleshooting.

---

## 📞 Getting Help

1. **Check Documentation**
   - README.md - overview
   - SETUP_GUIDE.md - installation
   - Code comments - implementation details

2. **Debug Locally**
   - Check backend logs
   - Check browser console (F12)
   - Check Etherscan for transaction status

3. **Verify Configuration**
   - All .env values present
   - All dependencies installed
   - All services running

4. **Review Code**
   - Services are well-commented
   - Error messages are descriptive
   - Test cases show expected behavior

---

## 🎓 Learning Path

### Beginner
1. Read PROJECT_SUMMARY.md
2. Follow SETUP_GUIDE.md
3. Run locally and test
4. Explore API at /docs

### Intermediate
1. Review smart contract code
2. Understand blockchain service
3. Explore verification logic
4. Study test cases

### Advanced
1. Modify smart contract features
2. Add authentication to backend
3. Implement file encryption
4. Deploy to production

---

## 📝 Next Steps

1. **Immediate**: Follow [SETUP_GUIDE.md](./SETUP_GUIDE.md) to set up locally
2. **Short-term**: Deploy to Sepolia and test with real files
3. **Medium-term**: Deploy to production using [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
4. **Long-term**: Add features, scale infrastructure, migrate to mainnet

---

## 🎉 You're Ready!

You now have a complete, production-ready blockchain file integrity system.

**Next step**: Read [SETUP_GUIDE.md](./SETUP_GUIDE.md) and start deploying!

---

**Project**: ChainGuard v1.0  
**Updated**: March 25, 2026  
**Status**: ✅ Complete and Ready to Deploy
