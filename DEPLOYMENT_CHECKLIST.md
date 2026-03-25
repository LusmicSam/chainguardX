# ChainGuard Deployment Checklist

## ✅ Pre-Deployment Setup

### API Keys & Credentials (DO THIS FIRST!)

- [ ] **Pinata Account**
  - [ ] API Key obtained from https://app.pinata.cloud/
  - [ ] Secret Key saved securely
  - [ ] JWT token generated
  - [ ] All permissions enabled

- [ ] **Alchemy/Infura RPC**
  - [ ] Created account at https://www.alchemy.com/
  - [ ] Created Sepolia testnet app
  - [ ] HTTPS RPC URL copied

- [ ] **Ethereum Wallet**
  - [ ] MetaMask installed
  - [ ] Wallet created
  - [ ] Switched to Sepolia testnet
  - [ ] Private key exported (SECURELY!)
  - [ ] Testnet ETH obtained from faucet (0.5+ ETH)

- [ ] **Etherscan (Optional)**
  - [ ] Account created at https://etherscan.io/
  - [ ] API key generated

---

## 🔗 Phase 1: Smart Contract Deployment

### Prerequisites
- [ ] Node.js 18+ installed
- [ ] npm installed
- [ ] All API keys from above ready

### Setup
- [ ] Navigate to `contracts/` directory
- [ ] `npm install` completed successfully
- [ ] Created `contracts/.env` with correct values:
  - [ ] `ALCHEMY_RPC_URL` filled
  - [ ] `DEPLOYER_PRIVATE_KEY` filled
  - [ ] `ETHERSCAN_API_KEY` filled (or empty if skipping)

### Compilation & Testing
- [ ] `npx hardhat compile` runs without errors
- [ ] `npx hardhat test` passes all tests
- [ ] Output shows:
  - [ ] ✓ Deployment
  - [ ] ✓ File Registration
  - [ ] ✓ File Verification
  - [ ] ✓ Ownership Transfer

### Deployment
- [ ] Network set to "Sepolia" in deploy script
- [ ] Deployer wallet has ETH (check with `npx hardhat run scripts/verify_deployment.js --network sepolia`)
- [ ] `npx hardhat run scripts/deploy.js --network sepolia` runs successfully
- [ ] **CONTRACT ADDRESS saved** (You'll need this!)
- [ ] Transaction hash noted for Etherscan lookup
- [ ] Block number recorded

### Post-Deployment
- [ ] ABI copied: `cp artifacts/contracts/FileRegistry.sol/FileRegistry.json ../backend/contract_abi/`
- [ ] Contract verified on Etherscan (optional but recommended)
- [ ] Test contract on Etherscan to confirm it's live

---

## 🐍 Phase 2: Backend Deployment

### Prerequisites
- [ ] Python 3.11+ installed
- [ ] pip installed
- [ ] All contract info from Phase 1 ready

### Environment Setup
- [ ] Created Python virtual environment: `python -m venv venv`
- [ ] Activated venv:
  - [ ] Windows: `venv\Scripts\activate`
  - [ ] Mac/Linux: `source venv/bin/activate`
- [ ] Verified venv is active (prompt shows `(venv)`)

### Dependencies
- [ ] `pip install -r requirements.txt` completed
- [ ] No errors during installation
- [ ] Key packages verified:
  - [ ] fastapi
  - [ ] uvicorn
  - [ ] web3
  - [ ] httpx
  - [ ] pydantic

### Configuration
- [ ] Created `backend/.env` with all values:
  - [ ] `PINATA_API_KEY` ✓
  - [ ] `PINATA_SECRET_KEY` ✓
  - [ ] `PINATA_JWT` ✓
  - [ ] `PINATA_GATEWAY_URL` ✓
  - [ ] `CONTRACT_ADDRESS` (from Phase 1) ✓
  - [ ] `BLOCKCHAIN_RPC_URL` ✓
  - [ ] `WALLET_PRIVATE_KEY` ✓
  - [ ] `CHAIN_ID=11155111` ✓
  - [ ] `MAX_FILE_SIZE_MB=50` ✓
  - [ ] `ALLOWED_EXTENSIONS` ✓

### File Structure
- [ ] `backend/contract_abi/FileRegistry.json` exists
- [ ] `backend/app/` directory structure complete
- [ ] All service files present
- [ ] All router files present

### Testing
- [ ] Backend starts: `uvicorn app.main:app --reload`
- [ ] No import errors
- [ ] Server runs on `http://0.0.0.0:8000`
- [ ] Swagger UI accessible at `http://localhost:8000/docs`

### Health Check
- [ ] Open http://localhost:8000/api/v1/health in browser
- [ ] Response shows:
  - [ ] `"status": "healthy"` or `"degraded"`
  - [ ] `"pinata_connected": true`
  - [ ] `"blockchain_connected": true`

If any are false:
- [ ] Verify .env values
- [ ] Check API keys haven't expired
- [ ] Verify network connectivity
- [ ] Check firewall settings

---

## ⚛️ Phase 3: Frontend Deployment

### Prerequisites
- [ ] Node.js 18+ installed
- [ ] npm installed
- [ ] Backend running on `http://localhost:8000`

### Setup
- [ ] Navigated to `frontend/` directory
- [ ] `npm install` completed successfully
- [ ] No dependency conflicts

### Configuration
- [ ] `frontend/src/services/api.js` updated:
  - [ ] `API_BASE` points to backend
  - [ ] Correct port if different from 8000

### Testing
- [ ] `npm run dev` starts successfully
- [ ] Vite development server runs
- [ ] Frontend accessible at `http://localhost:5173`
- [ ] No console errors

### UI Verification
- [ ] Dashboard loads without errors
- [ ] Navigation tabs visible (Upload, Registry, Retrieve)
- [ ] System health shows green checkmarks
- [ ] All icons display correctly

---

## 🧪 Phase 4: End-to-End Testing

### Test 1: Upload File
- [ ] Click "📤 Upload" tab
- [ ] Select a test file (PNG, PDF, or TXT)
- [ ] Drag or click to upload
- [ ] See "Uploading to IPFS..." message
- [ ] After ~30 seconds, see "✅ Upload Successful"
- [ ] Note the IPFS CID
- [ ] Note the transaction hash
- [ ] File size displays correctly

### Test 2: Verify in Registry
- [ ] Click "📋 Registry" tab
- [ ] See uploaded file listed
- [ ] File details show:
  - [ ] Correct file name
  - [ ] IPFS CID matches
  - [ ] File type correct
  - [ ] File size matches
- [ ] Click "Verify" button
- [ ] See ✅ **Verified** status

### Test 3: Retrieve File
- [ ] Click "🔍 Retrieve & Verify" tab
- [ ] Enter the file name (must match exactly)
- [ ] Click "🔍 Retrieve"
- [ ] See ✅ **VERIFIED** status
- [ ] File details display:
  - [ ] CID matches
  - [ ] Verified status: true
  - [ ] Size matches original
- [ ] Click "📥 Download"
- [ ] File downloads successfully

### Test 4: Check Blockchain
- [ ] Go to https://sepolia.etherscan.io/
- [ ] Search for contract address
- [ ] Verify contract is verified
- [ ] Check transaction history
- [ ] See file registration transactions

### Test 5: Multiple Files
- [ ] Upload 2-3 different files
- [ ] Verify each separately
- [ ] Check registry shows all files
- [ ] Verify they have different CIDs

---

## 🚀 Production Deployment

### Backend Deployment (Choose one)

#### Option A: Railway
- [ ] Account created at https://railway.app/
- [ ] New project created
- [ ] Connected to GitHub repository
- [ ] Environment variables configured:
  - [ ] All .env variables added to Railway
  - [ ] No hardcoded secrets
- [ ] Backend deployed
- [ ] Health check endpoint tested

#### Option B: Render
- [ ] Account created at https://render.com/
- [ ] New web service created
- [ ] GitHub connected
- [ ] Build and deploy settings configured
- [ ] Environment variables added
- [ ] Service deployed
- [ ] Public URL accessible

#### Option C: AWS EC2
- [ ] EC2 instance created (t2.small or larger)
- [ ] Ubuntu 22.04 LTS selected
- [ ] Security group configured (port 8000)
- [ ] Elastic IP assigned
- [ ] SSH access tested
- [ ] Python 3.11 installed
- [ ] Application deployed
- [ ] Systemd service created for auto-start

### Frontend Deployment (Choose one)

#### Option A: Vercel
- [ ] Account created at https://vercel.com/
- [ ] GitHub repository connected
- [ ] Project imported
- [ ] Build settings verified
- [ ] Environment variables set (API_BASE URL)
- [ ] Deployed to production
- [ ] Custom domain configured (optional)

#### Option B: Netlify
- [ ] Account created at https://netlify.com/
- [ ] Site created from GitHub
- [ ] Build settings configured
- [ ] Environment variables added
- [ ] Deploy triggered
- [ ] Preview and production URLs working

### Post-Deployment Verification
- [ ] Backend API accessible from public URL
- [ ] Frontend accessible from public URL
- [ ] Health check endpoint returns healthy status
- [ ] CORS properly configured for production domain
- [ ] File upload works from production frontend
- [ ] File retrieval works from production frontend
- [ ] SSL certificates active (https://)
- [ ] Monitoring alerts configured

---

## 🔒 Security Checklist

### Code Security
- [ ] No private keys in repository
- [ ] .env files in .gitignore
- [ ] Secrets never logged
- [ ] Input validation on all endpoints
- [ ] Rate limiting enabled (recommended)
- [ ] CORS properly configured
- [ ] SQL injection prevention (N/A - not using SQL)
- [ ] XSS prevention on frontend

### Deployment Security
- [ ] SSL/HTTPS enforced
- [ ] Firewall configured
- [ ] Security groups restricted
- [ ] Only necessary ports open
- [ ] Regular security updates applied
- [ ] Backups configured
- [ ] Monitoring and alerts set up
- [ ] Audit logging enabled

### Smart Contract Security
- [ ] Contract code reviewed
- [ ] No public mint/burn vulnerabilities
- [ ] Access control properly implemented
- [ ] No reentrancy vulnerabilities
- [ ] No overflow/underflow issues
- [ ] Contract verified on Etherscan
- [ ] Known contracts used (no experimental features)

---

## 📊 Monitoring & Maintenance

### Monitoring Setup
- [ ] Application logging enabled
- [ ] Error tracking configured (e.g., Sentry)
- [ ] API metrics collected
- [ ] Uptime monitoring configured
- [ ] Alerts configured for failures

### Regular Maintenance
- [ ] Weekly: Check system logs
- [ ] Weekly: Verify all endpoints working
- [ ] Monthly: Review security updates
- [ ] Monthly: Backup contract ABI and addresses
- [ ] Quarterly: Security audit
- [ ] Quarterly: Performance optimization

### Disaster Recovery
- [ ] Backup of contract address and ABI
- [ ] Backup of deployment addresses
- [ ] Rollback plan documented
- [ ] Recovery procedures documented
- [ ] Contact information for emergency support

---

## 📝 Documentation Updates

- [ ] README.md contains production URLs
- [ ] SETUP_GUIDE.md references production environment
- [ ] API documentation updated with production endpoints
- [ ] Runbook created for common operations
- [ ] Troubleshooting guide completed
- [ ] Architecture diagram updated
- [ ] Dependencies documented

---

## ✅ Final Verification

- [ ] All three components deployed and running
- [ ] End-to-end test passes in production
- [ ] All security checks completed
- [ ] Monitoring and alerts active
- [ ] Documentation complete and accurate
- [ ] Team trained on deployment
- [ ] Backup and recovery procedures tested
- [ ] Performance acceptable (< 2s response time)

---

## 🎉 Deployment Complete!

Once all checkboxes are marked, your ChainGuard production deployment is complete and ready for use.

### Post-Launch
- [ ] Share production URLs with stakeholders
- [ ] Monitor systems closely first 24 hours
- [ ] Be ready for quick bug fixes
- [ ] Gather user feedback
- [ ] Plan next features/improvements

---

**Deployment Date**: _______________  
**Deployer**: _______________  
**Approved By**: _______________  
**Notes**: ________________________________________________________________

---

For any issues, refer to:
- README.md
- SETUP_GUIDE.md
- Backend logs
- Frontend console (Dev Tools)
- Contract on Etherscan
