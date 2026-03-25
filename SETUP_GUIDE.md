# ChainGuard Setup Guide

Complete step-by-step guide to deploy and run ChainGuard.

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.11+** - Download from https://www.python.org/
- **Node.js 18+** - Download from https://nodejs.org/
- **Git** - Download from https://git-scm.com/
- **MetaMask** - Browser extension from https://metamask.io/
- **Code Editor** - VS Code, WebStorm, or your preferred editor

## 🔑 Get Required API Keys and Accounts

### Step 1: Create Pinata Account

1. Go to https://app.pinata.cloud/
2. Sign up for a free account
3. Navigate to **API Keys** section
4. Click **"Generate New Key"**
5. Ensure these permissions are enabled:
   - `pinFileToIPFS`
   - `pinJSONToIPFS`
   - `unpin`
6. Save these values (you'll need them in .env):
   - `PINATA_API_KEY`
   - `PINATA_SECRET_KEY`
   - `PINATA_JWT` (copy the JWT token)

### Step 2: Create Alchemy Account (Ethereum Node Provider)

1. Go to https://www.alchemy.com/
2. Sign up and create an account
3. Create a new app:
   - Select **Ethereum**
   - Select **Sepolia** testnet
4. Copy the **HTTPS RPC URL**
5. Save as `ALCHEMY_RPC_URL` in .env
6. Format: `https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY`

### Step 3: Create Ethereum Wallet

1. Install **MetaMask** browser extension
2. Create a new wallet (or use existing)
3. **Switch to Sepolia testnet:**
   - Click network selector
   - Enable "Show test networks"
   - Select "Sepolia"
4. **Export private key:**
   - Click account menu
   - Settings → Security & Privacy
   - Reveal Private Key → Copy
5. Save as `DEPLOYER_PRIVATE_KEY` in .env (without "0x" prefix)
6. **Get testnet ETH:**
   - Go to https://sepoliafaucet.com/
   - Enter your wallet address
   - Request 0.5 ETH (wait a few minutes)

### Step 4: Get Etherscan API Key (Optional)

1. Go to https://etherscan.io/apis
2. Create account and sign in
3. Create new API key
4. Save as `ETHERSCAN_API_KEY` in .env

## 📂 Project Setup

### Step 1: Clone or Download

```bash
# Download/clone the chainguard directory
cd chainguard
```

### Step 2: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: ChainGuard project"
```

## 🔗 Phase 1: Deploy Smart Contract

### Step 1: Install Hardhat Dependencies

```bash
cd contracts
npm install

# This installs:
# - hardhat
# - @nomicfoundation/hardhat-toolbox
# - dotenv
```

### Step 2: Configure Hardhat

Create/update `contracts/.env`:

```env
ALCHEMY_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
DEPLOYER_PRIVATE_KEY=your_wallet_private_key_without_0x_prefix
ETHERSCAN_API_KEY=your_etherscan_api_key
```

Replace with your actual values from Step 0.

### Step 3: Compile Contract

```bash
npx hardhat compile

# Output: artifacts/contracts/FileRegistry.sol/FileRegistry.json
```

### Step 4: Run Tests

```bash
npx hardhat test

# Output should show all tests passing
```

### Step 5: Deploy Contract

```bash
# Deploy to Sepolia testnet
npx hardhat run scripts/deploy.js --network sepolia

# ⏳ Wait 2-3 minutes for deployment
# Output will show:
# ✅ FileRegistry deployed to: 0x...
# Contract address: 0xAbCdEf...
# Block number: 12345678

# SAVE THIS CONTRACT ADDRESS - YOU'LL NEED IT!
```

### Step 6: Copy Contract ABI to Backend

```bash
# From the contracts directory:
cp artifacts/contracts/FileRegistry.sol/FileRegistry.json ../backend/contract_abi/

# This provides the contract interface to the backend
```

## 🐍 Phase 2: Setup Backend (Python FastAPI)

### Step 1: Navigate to Backend

```bash
cd ../backend
```

### Step 2: Create Python Virtual Environment

```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt

# This installs:
# - fastapi, uvicorn (web framework)
# - web3.py (blockchain interaction)
# - httpx (HTTP client for Pinata)
# - pydantic (data validation)
# - And more...
```

### Step 4: Configure Backend .env

Edit `backend/.env` and replace with your actual values:

```env
# From Pinata API Keys page
PINATA_API_KEY=your_pinata_api_key
PINATA_SECRET_KEY=your_pinata_secret_key
PINATA_JWT=your_pinata_jwt_token
PINATA_GATEWAY_URL=https://gateway.pinata.cloud/ipfs/

# From Phase 1 deployment
CONTRACT_ADDRESS=0xYourContractAddressFromDeployment

# From Alchemy
BLOCKCHAIN_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY

# Your wallet private key
WALLET_PRIVATE_KEY=your_private_key_without_0x

# Sepolia chain ID
CHAIN_ID=11155111

# Application settings
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=.png,.jpg,.jpeg,.gif,.pdf,.json,.csv,.txt,.doc,.docx
```

### Step 5: Run Backend

```bash
# Make sure you're in the backend directory and venv is activated
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Output:
# Uvicorn running on http://0.0.0.0:8000
# Application startup complete
```

### Step 6: Test Backend API

Open http://localhost:8000/docs in your browser

- You should see the Swagger UI
- Try the `/api/v1/health` endpoint
- Look for green checkmarks next to "Pinata" and "Blockchain"

If health check fails:
- Check your .env values
- Verify PINATA_JWT is not expired
- Verify BLOCKCHAIN_RPC_URL is accessible
- Check firewall settings

## ⚛️ Phase 3: Setup Frontend (React)

### Step 1: Navigate to Frontend

```bash
cd ../frontend
```

### Step 2: Install Node Dependencies

```bash
npm install

# This installs:
# - react, react-dom
# - vite (build tool)
# - axios (HTTP client)
# - react-dropzone (file upload UI)
# - react-hot-toast (notifications)
```

### Step 3: Update API URL (if needed)

Edit `frontend/src/services/api.js`:

```javascript
const API_BASE = "http://localhost:8000/api/v1";
// Change if your backend is on a different address
```

### Step 4: Run Frontend

```bash
npm run dev

# Output:
#   VITE v5.0.8  ready in X ms
#   ➜  Local:   http://localhost:5173/
```

### Step 5: Open Dashboard

Go to http://localhost:5173 in your browser

You should see:
- ChainGuard title
- 🟢 System health (Pinata ✅, Blockchain ✅)
- Three tabs: Upload, Registry, Retrieve & Verify

## 🧪 Test End-to-End

### 1. Upload a File

1. Click **📤 Upload** tab
2. Drag and drop or select a small test file (PNG, PDF, etc.)
3. Wait for:
   - ⏳ "Uploading to IPFS..." (30 seconds)
   - ✅ "File registered on blockchain!"
4. Note the IPFS CID and transaction hash

### 2. Verify File in Registry

1. Click **📋 Registry** tab
2. You should see your uploaded file
3. Click "Verify" button on the file
4. Should show ✅ **Verified** status

### 3. Retrieve and Download

1. Click **🔍 Retrieve & Verify** tab
2. Enter the file name (exactly as shown in registry)
3. Click "🔍 Retrieve"
4. Should show ✅ **VERIFIED** and display file details
5. Click "📥 Download Verified File"
6. File should download

## 🚀 Running All Components Together

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

### Terminal 3: Monitor Logs

```bash
# Optional - in a third terminal, you can watch contract events or logs
cd contracts
npx hardhat node  # For local testing (optional)
```

## 📝 Common Issues and Solutions

### Issue: "Contract not found" Error

**Solution:**
1. Verify `CONTRACT_ADDRESS` in backend/.env is correct
2. Check that contract was deployed to Sepolia (not localhost)
3. Ensure `FileRegistry.json` exists in `backend/contract_abi/`

### Issue: "Pinata authentication failed"

**Solution:**
1. Verify `PINATA_JWT` token is not expired
2. Generate a new JWT token from https://app.pinata.cloud/
3. Check that API key has required permissions

### Issue: "Backend connection refused"

**Solution:**
1. Ensure backend is running on port 8000
2. Check firewall isn't blocking localhost:8000
3. Verify no other process is using port 8000

### Issue: "No ETH in wallet"

**Solution:**
1. Go to https://sepoliafaucet.com/
2. Enter your MetaMask wallet address
3. Wait 5-10 minutes for ETH to arrive
4. Check balance in MetaMask

### Issue: "Frontend can't connect to backend"

**Solution:**
1. Verify backend is running and healthy
2. Check `frontend/src/services/api.js` has correct URL
3. Ensure CORS is enabled in backend (it is by default)
4. Check browser console for error messages

## 🔒 Security Considerations

### DO NOT

- ❌ Commit `.env` files with real private keys to Git
- ❌ Share your private key with anyone
- ❌ Use mainnet private key for testing
- ❌ Expose API keys in frontend code

### DO

- ✅ Use `.gitignore` to exclude .env files
- ✅ Always use testnet for development
- ✅ Rotate API keys periodically
- ✅ Use environment variables for secrets
- ✅ Review contract code before deployment

## 📦 Docker Deployment

If you want to use Docker:

```bash
# Build and run all services
docker-compose up --build

# Services will be available at:
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 🎯 Next Steps

1. **Explore the API**:
   - Open http://localhost:8000/docs
   - Try different endpoints
   - Read the API documentation

2. **Review the Code**:
   - Check `backend/app/services/` to understand architecture
   - Review `frontend/src/components/` for React patterns
   - Study `contracts/contracts/FileRegistry.sol` to understand blockchain logic

3. **Deploy to Production**:
   - Follow the deployment section in README.md
   - Set up continuous integration/deployment
   - Use environment-specific configurations

4. **Add Features**:
   - User authentication
   - File encryption
   - Advanced analytics
   - Rate limiting

## 📞 Support

If you encounter issues:

1. Check this guide again
2. Review the README.md
3. Check logs in terminal
4. Verify .env configuration
5. Test health endpoints

---

**Congratulations!** 🎉 You have successfully deployed ChainGuard!

Your blockchain-verified file integrity system is now running and ready to use.
