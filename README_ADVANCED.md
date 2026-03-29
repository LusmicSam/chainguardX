# 🔗 ChainGuard: Cryptographically Verifiable CDN

> **Blockchain-backed file integrity verification system combining IPFS, Ethereum smart contracts, and a FastAPI proxy for trustless file delivery.**

---

## 🎯 Executive Summary

ChainGuard solves **digital asset tampering** in distributed networks by creating an immutable audit trail of files. Clients can **cryptographically prove** that files haven't been altered, combining:
- 🌐 **IPFS** (Pinata) for decentralized storage
- ⛓️ **Ethereum** blockchain for immutable records
- 🔍 **Content hashing** for verification
- ⚡ **FastAPI proxy** as the access node

**Result**: A next-generation CDN where trust is mathematically proven, not assumed.

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        END USER INTERFACE                        │
│                    (React + Vite Dashboard)                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   API GATEWAY / PROXY LAYER                      │
│                     (FastAPI Backend)                            │
│  ┌──────────────┬────────────────┬──────────────┬────────────┐  │
│  │   Upload     │   Retrieval    │   Registry   │   Health   │  │
│  │  /upload     │  /file/{name}  │ /registry    │   /health  │  │
│  │              │  /verify/{name}│ /registry/{n}│            │  │
│  └──────────────┴────────────────┴──────────────┴────────────┘  │
│  ┌──────────────────┬──────────────────┬──────────────────┐     │
│  │ PinataService    │ BlockchainService│VerificationSvc   │     │
│  │ (IPFS Ops)       │ (Smart Contract) │ (Verification)   │     │
│  └──────────────────┴──────────────────┴──────────────────┘     │
└──────────────┬──────────────────────────────────────────────────┘
               │                                    │
               ▼                                    ▼
    ┌──────────────────┐            ┌──────────────────────────┐
    │  PINATA / IPFS   │            │  ETHEREUM BLOCKCHAIN     │
    │  Content Store   │            │  Smart Contract Ledger   │
    │  (Decentralized) │            │  (Sepolia Testnet)       │
    └──────────────────┘            └──────────────────────────┘
         CID Storage                    CID → Filename Mapping
                                        Immutable Audit Trail
```

---

## 🔄 Data Flow Diagrams

### Upload Flow (Write Path)

```
┌────────────┐
│   Client   │
│  File (.jpg)
└─────┬──────┘
      │
      ▼
┌──────────────────────────┐
│  Frontend Upload Form    │
│  - File validation       │
│  - Progress tracking     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  POST /upload            │
│  (FastAPI Endpoint)      │
└────────────┬─────────────┘
             │ Multipart Form
             ▼
┌──────────────────────────┐
│  PinataService           │
│  - Upload to Pinata      │
│  - Return CID            │
└────────────┬─────────────┘
      CID: QmXxxx...
             │
             ▼
┌──────────────────────────┐
│  BlockchainService       │
│  - Call registerFile()   │
│  - Sign transaction      │
│  - Wait for confirmation │
└────────────┬─────────────┘
   TX: 0x1234...
             │
             ▼
┌──────────────────────────┐
│  Response to Client      │
│  ✅ Upload Success       │
│  - CID: QmXxxx...       │
│  - TX Hash              │
│  - Blockchain Address   │
└──────────────────────────┘
```

### Retrieval & Verification Flow (Read Path)

```
┌────────────┐
│   Client   │
│   GET /file/document.pdf
└─────┬──────┘
      │
      ▼
┌──────────────────────────────────┐
│  FastAPI Proxy                   │
│  GET /file/{filename}            │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  BlockchainService               │
│  Query: getCID(filename)         │
│  Result: QmXxxx... (true CID)    │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  PinataService                   │
│  Fetch: IPFS://QmXxxx...         │
│  Result: File bytes + CID        │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  VerificationService             │
│  1. Compute hash of fetched file │
│  2. Compare with blockchain CID  │
│  3. Return: VERIFIED or REJECTED │
└────────────┬─────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
   MATCH ✅      MISMATCH ❌
   Return        Return 403
   File +        Forbidden
   Headers       + Error
```

### Verification-Only Flow (CID Verification)

```
┌────────────┐
│   Client   │
│ CID: QmXxxx...
└─────┬──────┘
      │
      ▼
┌──────────────────────────────────┐
│  POST /verify-cid                │
│  { cid: "QmXxxx..." }            │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  VerificationService             │
│  Check: Is CID in blockchain?    │
│  Match against registered CIDs   │
└────────────┬─────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
   FOUND ✅      NOT FOUND ❌
   Return        Return 404
   { verified:    { verified:
     true }       false }
```

---

## 🖼️ Frontend Wireframes

### Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  🔗 ChainGuard Dashboard          [Health: ✅ Connected]    │
├─────────────────────────────────────────────────────────────┤
│  ┌─ TABS ─────────────────────────────────────────────────┐ │
│  │ [📤 Upload] [📋 Registry] [📥 Retrieve] [⚙️ Settings]  │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📤 FILE UPLOAD                                     │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                     │   │
│  │   ┌─────────────────────────────────────────────┐  │   │
│  │   │  Drag files here or click to select         │  │   │
│  │   │  📁 Supported: .pdf, .jpg, .png, .zip      │  │   │
│  │   │  Max size: 100MB                           │  │   │
│  │   └─────────────────────────────────────────────┘  │   │
│  │                                                     │   │
│  │   [🔗 Upload & Register]                           │   │
│  │                                                     │   │
│  │   Recent: document.pdf   ✅ Uploaded              │   │
│  │           image.jpg      ✅ Verified              │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Registry Tab

```
┌─────────────────────────────────────────────────────────────┐
│  📋 FILE REGISTRY                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Filename              CID             Status    Actions   │
│  ─────────────────────────────────────────────────────────  │
│  report.pdf           QmXxxx1...      ✅ ✅      [🔍 Verify]│
│  logo.png             QmXxxx2...      ✅ ✅      [📥 Get]   │
│  dataset.csv          QmXxxx3...      ⏳ ❓      [⟳ Check]  │
│  archive.zip          QmXxxx4...      ✅ ✅      [🔗 Link]  │
│                                                             │
│  Filter: [All ▼]  Search: [________]  [Search]             │
│                                                             │
│  Page: [< 1 >]  Total: 4 files       Last updated: 2m ago │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Retrieval & Verification Tab

```
┌─────────────────────────────────────────────────────────────┐
│  📥 RETRIEVE & VERIFY                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Option 1: Retrieve by Filename                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Filename: [report.pdf____________]  [Search]      │    │
│  │  Checking blockchain...                            │    │
│  │  Found: QmXxxx... (20.5 KB)                        │    │
│  │  Status: ✅ VERIFIED & AUTHENTIC                   │    │
│  │  [📥 Download File]  [🔗 Get IPFS Link]           │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  Option 2: Verify by CID                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  CID: [QmXxxx..._________________]  [Verify]       │    │
│  │                                                     │    │
│  │  Result:                                           │    │
│  │  ✅ VERIFIED: This CID is registered on blockchain│    │
│  │  Associated file: report.pdf                       │    │
│  │  Registered: 2024-03-25 10:30 UTC                 │    │
│  │  Uploader: 0x1234...                              │    │
│  │                                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security & Trust Model

### Verification Chain of Trust

```
TRUST HIERARCHY
===============

Level 1: IMMUTABLE RECORD
         ┌──────────────────────────┐
         │  Ethereum Blockchain     │
         │  Immutable ledger:       │
         │  filename → CID mapping  │
         │  Timestamp               │
         │  Uploader address        │
         └──────────────────────────┘
         ▲
         │ (Cannot be changed, cryptographically signed)
         │

Level 2: CONTENT VERIFICATION
         ┌──────────────────────────┐
         │  Content Hash (CID)      │
         │  SHA-256 based           │
         │  Deterministic           │
         │  Content-addressed       │
         └──────────────────────────┘
         ▲
         │ (Any change to file changes hash)
         │

Level 3: DELIVERY VERIFICATION
         ┌──────────────────────────┐
         │  Client-side Comparison  │
         │  Hash blockchain CID     │
         │  Against received file   │
         │  Mathematical proof      │
         └──────────────────────────┘
         ▲
         │ (No trust required, math is proof)
         │

Result: CRYPTOGRAPHIC PROOF OF AUTHENTICITY
        No intermediary can tamper without detection
```

### Attack Scenarios & Defenses

```
ATTACK SCENARIO 1: File Tampering
──────────────────────────────────
Attacker:  Modifies file on IPFS
Defense:   New content → different CID → mismatch detected
Result:    ✅ DETECTED & REJECTED


ATTACK SCENARIO 2: Stale Cache Serving
────────────────────────────────────────
Attacker:  Proxy serves old file version
Defense:   Old file has old CID → doesn't match blockchain
Result:    ✅ DETECTED & REJECTED


ATTACK SCENARIO 3: Blockchain Record Fakery
─────────────────────────────────────────────
Attacker:  Creates fake smart contract
Defense:   Owner must sign registerFile() transaction
           Only owner's wallet can register
           All on public Ethereum (auditable)
Result:    ✅ OWNER-ONLY PROTECTION


ATTACK SCENARIO 4: Man-in-the-Middle
─────────────────────────────────────
Attacker:  Intercepts file during transmission
Defense:   Client verifies hash matches blockchain
           Even if intercepted, client math proves tampering
Result:    ✅ DETECTED IMMEDIATELY
```

---

## 📊 Component Interaction Diagram

### System Components & Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  React Component Tree                                  │ │
│  │  ┌──────────┬─────────────┬──────────────┬──────────┐  │ │
│  │  │  Upload  │   Registry  │  Retrieval   │ Badge    │  │ │
│  │  └──────────┴─────────────┴──────────────┴──────────┘  │ │
│  │              ▼ (all use)                                 │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │  api.js - Axios HTTP Client                    │   │ │
│  │  │  - uploadFile()                                │   │ │
│  │  │  - retrieveFile()                              │   │ │
│  │  │  - verifyFile()                                │   │ │
│  │  │  - listFiles()                                 │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST (POST, GET)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND API LAYER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  FastAPI Main App (main.py)                            │ │
│  │  - CORS Middleware                                     │ │
│  │  - Request validation                                 │ │
│  │  - Route registration                                 │ │
│  └─────────────┬────────────────────────────────────────┘ │
│                │                                           │
│  ┌─────────────┼────────────────────────────────────────┐ │
│  │             ▼                                         │ │
│  │  ┌──────────────────┬──────────────┬───────────────┐ │ │
│  │  │ upload.py        │ retrieve.py  │ registry.py   │ │ │
│  │  │ POST /upload     │ GET /file    │ GET /registry │ │ │
│  │  │                  │ GET /verify  │               │ │ │
│  │  └──────────────────┴──────────────┴───────────────┘ │ │
│  │             │
│  │  ┌──────────┴──────────────────────────────────────┐ │ │
│  │  │              SERVICES LAYER                     │ │ │
│  │  ├──────────────────────────────────────────────┤ │ │
│  │  │                                              │ │ │
│  │  │  PinataService            BlockchainService  │ │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐   │ │ │
│  │  │  │ upload_file()   │  │ register_file() │   │ │ │
│  │  │  │ fetch_file()    │  │ get_file_cid()  │   │ │ │
│  │  │  │ list_pins()     │  │ verify_file()   │   │ │ │
│  │  │  │ unpin_file()    │  │ transfer_owner()│   │ │ │
│  │  │  └─────────────────┘  └─────────────────┘   │ │ │
│  │  │                                              │ │ │
│  │  │  VerificationService                        │ │ │
│  │  │  ┌──────────────────────────────────────┐   │ │ │
│  │  │  │ verify_and_fetch()                  │   │ │ │
│  │  │  │ verify_only()                       │   │ │ │
│  │  │  │ compute_sha256()                    │   │ │ │
│  │  │  │ compute_ipfs_cid()                  │   │ │ │
│  │  │  └──────────────────────────────────────┘   │ │ │
│  │  │                                              │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  └─────────────┬───────────────────────────────────────┘ │
│                │ (async HTTP calls + Smart Contract)     │
└─────────────────┼──────────────────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
┌──────────────────┐  ┌─────────────────┐
│  PINATA / IPFS   │  │ ETHEREUM CHAIN  │
│  REST API        │  │ Web3 Provider   │
│  Content Storage │  │ Smart Contract  │
│  /upload         │  │ /call           │
│  /retrieve       │  │ /sendTransaction│
└──────────────────┘  └─────────────────┘
```

---

## 🧩 API Endpoints Map

### Endpoint Topology

```
BASE_URL: http://localhost:8000

FILE MANAGEMENT
├── POST   /upload                    [Create new file entry]
│           Query: --
│           Body: { file: multipart }
│           Returns: { cid, tx_hash, block_address }
│
├── GET    /file/{name}               [Retrieve & verify file]
│           Params: filename
│           Query: --
│           Returns: File bytes (if verified)
│           Headers: X-ChainGuard-Status, X-ChainGuard-CID
│
└── POST   /verify-cid                [Verify CID authenticity]
            Body: { cid: "QmXxxx..." }
            Returns: { verified, filename }


REGISTRY MANAGEMENT
├── GET    /registry                  [List all files]
│           Query: --
│           Returns: [{ name, cid, timestamp, uploader }]
│
├── GET    /registry/{name}/history   [File version history]
│           Params: filename
│           Returns: [{ cid, tx_hash, timestamp }]
│
└── GET    /registry/{name}/verify    [Verify specific file]
             Params: filename
             Returns: { verified, cid, timestamp }


SYSTEM HEALTH
└── GET    /health                    [System status check]
            Returns: { status: "ok", components: {...} }
            Fields: pinata_connected, blockchain_connected, etc.
```

---

## 🔐 Smart Contract State Diagram

### FileRegistry.sol State Transitions

```
                    ┌─────────────────┐
                    │  Initial State  │
                    │  (Empty)        │
                    └────────┬────────┘
                             │
                             │ registerFile(name, cid)
                             │ [owner only]
                             ▼
                    ┌─────────────────┐
                    │  File Registered│
                    │  name → CID     │
                    │  timestamp set  │
                    │  version = 1    │
                    └────────┬────────┘
                      │      │ │
         ┌────────────┘      │ └────────────┐
         │                   │              │
    Can Query          Update File    Transfer Owner
    (verifyFile)       registerFile    (transferOwnership)
         │             (same owner)          │
         │                   │               │
         ▼                   ▼               ▼
    ┌─────────┐        ┌──────────┐   ┌──────────────┐
    │ Verify  │        │ Version+ │   │ New Owner    │
    │ Success │        │ CID Update   │ Recorded     │
    │ ✅      │        │ event emit   │ event emit   │
    └─────────┘        │ ✅      │   └──────────────┘
                       └────┬────┘
                            │
                   ┌────────┴─────────┐
                   │                  │
              Still Queryable    Can Update Again
              (all versions)     or Transfer
```

---

## 📈 Data Model & Schema

### Core Data Structures

```
BLOCKCHAIN RECORD (FileRegistry.sol)
════════════════════════════════════
FileRecord struct {
  ├─ name: string                 // Human-readable filename
  ├─ cid: string                  // IPFS Content Identifier
  ├─ timestamp: uint256            // Block timestamp
  ├─ uploader: address             // Wallet address of uploader
  ├─ versions: uint256             // Count of updates
  └─ active: bool                  // Is this file active?
}

Mappings:
  ├─ files: address → (filename → FileRecord)
  ├─ fileNames: address → string[]   // All files by owner
  └─ cidToFile: string → FileRecord  // CID lookup


API SCHEMA (Pydantic Models)
═════════════════════════════
FileUploadResponse {
  ├─ filename: str
  ├─ cid: str                     // IPFS CID
  ├─ tx_hash: str                 // Blockchain transaction
  ├─ block_number: int
  ├─ timestamp: str
  └─ status: str                  // "success" | "pending" | "error"
}

VerificationStatus {
  ├─ verified: bool               // CID matches blockchain
  ├─ filename: str
  ├─ cid: str
  ├─ blockchain_record: dict
  ├─ timestamp_blockchain: str
  └─ timestamp_retrieved: str
}

FileListResponse {
  ├─ total_files: int
  ├─ files: [
  │   ├─ name: str
  │   ├─ cid: str
  │   ├─ timestamp: str
  │   ├─ uploader: str
  │   └─ version_count: int
  │ ]
  └─ chain_id: int
}


IPFS/PINATA METADATA
════════════════════
PinataResponse {
  ├─ IpfsHash: str                // CID (QmXxxx...)
  ├─ PinSize: int                 // File size in bytes
  ├─ Timestamp: str               // ISO timestamp
  ├─ MimeType: str
  └─ Name: str
}
```

---

## 🚀 Deployment Architecture

### Multi-Environment Setup

```
LOCAL DEVELOPMENT
═════════════════
Frontend: http://localhost:5173 (Vite dev server)
Backend:  http://localhost:8000 (FastAPI dev)
Contract: Hardhat local chain (chainId: 31337)
IPFS:     Pinata API (testnet keys)
┌─────────────────────────────────────────────┐
│ All services run locally, fast iteration    │
│ Mock blockchain for testing                 │
│ Pinata testnet for file storage             │
└─────────────────────────────────────────────┘


TESTNET STAGING
═══════════════
Frontend: https://staging-chainguard.example.com
Backend:  https://api-staging.example.com
Contract: Ethereum Sepolia (chainId: 11155111)
IPFS:     Pinata (production keys)
┌─────────────────────────────────────────────┐
│ Real blockchain, real IPFS                  │
│ Testnet ETH (from faucet)                   │
│ Same code as production                     │
│ Verification before production              │
└─────────────────────────────────────────────┘


PRODUCTION
══════════
Frontend: https://chainguard.example.com
Backend:  https://api.example.com
Contract: Ethereum Mainnet (chainId: 1)
IPFS:     Pinata (production keys)
┌─────────────────────────────────────────────┐
│ Real blockchain, real IPFS, real ETH        │
│ Load balancing & scaling                    │
│ Monitoring & alerting                       │
│ CDN for frontend static assets              │
│ Auto-scaling backend                        │
└─────────────────────────────────────────────┘
```

### Docker Compose Stack

```
docker-compose.yml
════════════════════

┌────────────────────────────────────────────────┐
│  services:                                     │
│                                                │
│  backend                                       │
│  ├─ Image: chainguard-backend:latest           │
│  ├─ Port: 8000:8000                            │
│  ├─ Volumes: [./backend:/app]                  │
│  ├─ Env: [.env.backend loaded]                 │
│  ├─ Health: GET /health every 10s              │
│  └─ Depends: (none)                            │
│                                                │
│  frontend                                      │
│  ├─ Image: chainguard-frontend:latest          │
│  ├─ Port: 5173:5173                            │
│  ├─ Volumes: [./frontend:/app]                 │
│  ├─ Env: VITE_API_URL=http://backend:8000      │
│  ├─ Health: GET / every 10s                    │
│  └─ Depends: backend (healthy)                 │
│                                                │
│  networks:                                     │
│  └─ chainguard-network (bridge)                │
│                                                │
└────────────────────────────────────────────────┘
```

---

## 🔄 Workflow Sequences

### Complete Upload-to-Verification Sequence

```
TIMELINE: Upload → Register → Retrieve → Verify
═══════════════════════════════════════════════════

T0: USER ACTION
    │
    └─→ Client selects file: "report.pdf" (2.5MB)

T1: FRONTEND VALIDATION
    │
    └─→ FileUpload component checks:
        ├─ File size < 100MB ✅
        ├─ Extension in ALLOWED_EXTENSIONS ✅
        └─ File not empty ✅

T2: UPLOAD REQUEST
    │
    └─→ POST /upload with multipart form data
        Headers: Content-Type: multipart/form-data

T3: BACKEND RECEIVES
    │
    └─→ main.py receives request
        ├─ Validates Pydantic schema
        ├─ Routes to upload.py handler
        └─ Initializes PinataService

T4: IPFS UPLOAD
    │
    └─→ PinataService.upload_file()
        ├─ Multipart upload to Pinata
        ├─ Returns CID: "QmAbc123..."
        └─ File now stored on IPFS

T5: BLOCKCHAIN REGISTRATION
    │
    └─→ BlockchainService.register_file()
        ├─ Build transaction data
        ├─ Call FileRegistry.registerFile()
        ├─ Sign with wallet private key
        ├─ Broadcast to Sepolia network
        ├─ Wait for confirmation (15-30s)
        └─ Returns tx_hash: "0x1234..."

T6: RESPONSE TO CLIENT
    │
    └─→ Upload successful
        ├─ CID: QmAbc123...
        ├─ Filename: report.pdf
        ├─ Tx: 0x1234...
        ├─ Block: 4,521,234
        └─ Status: ✅ REGISTERED

T7-15: FILE IMMUTABLE ON BLOCKCHAIN
    │    (CID cannot be changed)
    │    (Visible in Etherscan)
    │
    └─→ [Time passes... client returns later]

T16: USER RETRIEVAL REQUEST
    │
    └─→ Client clicks "Get report.pdf"

T17: RETRIEVE REQUEST
    │
    └─→ GET /file/report.pdf

T18: BLOCKCHAIN QUERY
    │
    └─→ BlockchainService.get_file_cid()
        ├─ Query smart contract
        ├─ Return true CID: QmAbc123...
        └─ Ensure file hasn't been updated

T19: IPFS FETCH
    │
    └─→ PinataService.fetch_file(QmAbc123...)
        ├─ Retrieve file from IPFS
        ├─ Compute CID of downloaded bytes
        ├─ Return file data
        └─ Return computed CID: QmAbc123...

T20: VERIFICATION
    │
    └─→ VerificationService.verify_and_fetch()
        ├─ Compare blockchain CID vs fetched CID
        ├─ BlockchainCID: QmAbc123...
        ├─ FetchedCID:    QmAbc123...
        ├─ Match? YES ✅
        └─ Set verification headers

T21: RESPONSE TO CLIENT
    │
    └─→ Return file with headers
        ├─ X-ChainGuard-Status: VERIFIED ✅
        ├─ X-ChainGuard-CID: QmAbc123...
        ├─ X-ChainGuard-Blockchain-Verified: true
        └─ File content (binary)

T22: CLIENT SUCCESS
    │
    └─→ File downloaded + VerificationBadge shows ✅ VERIFIED
        User has mathematical proof file hasn't changed
```

---

## 🛡️ Security Matrix

### Security Controls by Layer

```
┌────────────────────────────────────────────────────────┐
│ LAYER              THREAT               CONTROL         │
├────────────────────────────────────────────────────────┤
│ Frontend           XSS Attack           CSP Headers     │
│                    CSRF                 Token Validation│
│                    Code Injection       Input Sanitize  │
├────────────────────────────────────────────────────────┤
│ API                SQL Injection        Pydantic Schema │
│                    DDOS                 Rate Limiting   │
│                    Unauth Access        CORS Middleware │
├────────────────────────────────────────────────────────┤
│ Services           File Tampering       CID Verification│
│                    Replay Attack        Timestamp Check │
│                    Service Hijack       HTTPS + mTLS    │
├────────────────────────────────────────────────────────┤
│ Blockchain         Replay Attack        Nonce Increment │
│                    Frontrunning         Owner Check     │
│                    Reentrancy           No External Calls
├────────────────────────────────────────────────────────┤
│ IPFS               Content Modification Content Hash    │
│                    Pinning Failure      Redundancy      │
│                    Gateway Down         Fallback URLs   │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Performance & Scalability

### Request Timing Analysis

```
OPERATION: Upload New File (2.5MB)
═════════════════════════════════════

Step                              Time      Cumulative
─────────────────────────────────────────────────────
1. Frontend validation            50ms      50ms
2. Transfer to backend            100ms     150ms
3. Write to temp storage          30ms      180ms
4. Hash computation (SHA256)      200ms     380ms
5. Upload to Pinata               2-4s      2.4-4.4s
6. Smart contract call setup      100ms     2.5-4.5s
7. Transaction broadcast          500ms     3.0-5.0s
8. Wait for confirmation          15-30s    18-35s
9. Response formatting            50ms      18-35s
10. Return to client              50ms      18-35s

TOTAL: ~18-35 seconds (blockchain confirmation limited)


OPERATION: Retrieve & Verify Existing File
═════════════════════════════════════════════

Step                              Time      Cumulative
─────────────────────────────────────────────────────
1. Blockchain CID query           300ms     300ms
2. Fetch from Pinata              1-3s      1.3-3.3s
3. Hash computation               200ms     1.5-3.5s
4. Hash comparison                10ms      1.5-3.5s
5. Response formatting            50ms      1.5-3.5s

TOTAL: ~1.5-3.5 seconds (IPFS fetch is bottleneck)


OPTIMIZATION OPPORTUNITIES
═══════════════════════════
- Pinata region selection (closer = faster)
- Caching layer (Redis) for frequently accessed files
- Batch transactions (group multiple uploads)
- IPFS gateway redundancy (Cloudflare, Infura)
- HTTP/2 multiplexing
- Gzip compression
- CDN layer for frontend
```

---

## 🔗 Technology Stack Overview

### Full Stack Breakdown

```
TIER              TECHNOLOGY          VERSION    PURPOSE
─────────────────────────────────────────────────────────────
Frontend UI       React               18.2       Component rendering
                  Vite                5.0        Build & dev server
                  Axios               1.6        HTTP client
                  React Dropzone      14.2       File upload UX
                  React Hot Toast     2.4        Notifications

Backend API       FastAPI             0.104.1    REST framework
                  Uvicorn             0.24.0     ASGI server
                  Pydantic            2.5.0      Data validation
                  Python              3.11+      Runtime
                  Httpx               0.25.2     Async HTTP

Blockchain        Solidity            0.8.19     Smart contract
                  Hardhat             2.19.0     Dev framework
                  Ethers.js           6.10.0     JS interaction
                  Web3.py             6.13.0     Python interaction
                  Ethereum Sepolia    Network    Testnet

Storage           IPFS/Pinata         API        Content addressing
                  Sha256              Crypto     Content hashing

Infrastructure    Docker              24.0       Containerization
                  Docker Compose      2.24.0     Orchestration
                  Git                 2.42       Version control

Testing           Pytest              7.4        Python tests
                  Hardhat Tests       2.19       Contract tests
                  Jest                29.0       JS tests (optional)
```

---

## 🎓 Learning Paths

### Different User Journeys

```
DEVELOPER (Software Engineer)
─────────────────────────────
1. Read: README.md, PROJECT_SUMMARY.md
2. Setup: Follow SETUP_GUIDE.md (Phase 1-2)
3. Explore: Read smart contract, backend services
4. Test: Unit tests, then end-to-end tests
5. Deploy: Follow DEPLOYMENT_CHECKLIST.md (Phase 1-2)
6. Scale: Add features, optimize performance

Timeline: ~1 week


ARCHITECT (System Designer)
──────────────────────────────
1. Read: README.md (Architecture section)
2. Study: High-level diagrams (this document)
3. Analyze: Security model & trust model
4. Evaluate: Scalability & performance analysis
5. Review: DEPLOYMENT_CHECKLIST.md (Phase 0)
6. Plan: Production architecture

Timeline: ~2-3 days


OPERATOR (DevOps/Infrastructure)
──────────────────────────────────
1. Read: DEPLOYMENT_CHECKLIST.md
2. Setup: Docker Compose, CI/CD
3. Configure: Environment variables
4. Deploy: Local → Staging → Production
5. Monitor: Health checks, alerting
6. Scale: Load balancing, auto-scaling

Timeline: ~1 week


AUDITOR (Security/Compliance)
──────────────────────────────
1. Read: Security section (this doc)
2. Review: Smart contract security analysis
3. Test: Attack scenarios & defenses
4. Audit: Code quality & dependencies
5. Verify: Data privacy & encryption
6. Report: Security posture assessment

Timeline: ~2 weeks
```

---

## 📚 Documentation Index

All resources in this project:

```
ROOT
├── README.md                      [You are here - comprehensive overview]
├── README_ADVANCED.md             [This file - diagrams & architecture]
├── SETUP_GUIDE.md                 [Step-by-step setup instructions]
├── PROJECT_SUMMARY.md             [What was built & why]
├── DEPLOYMENT_CHECKLIST.md        [Pre-deployment verification]
├── INDEX.md                       [Navigation guide]
│
├── contracts/
│   ├── FileRegistry.sol           [Smart contract source code]
│   ├── test/FileRegistry.test.js  [Contract tests]
│   └── scripts/deploy.js          [Deployment script]
│
├── backend/
│   ├── app/
│   │   ├── main.py               [FastAPI app entry point]
│   │   ├── config.py             [Configuration management]
│   │   ├── models/schemas.py     [Pydantic models]
│   │   ├── services/             [Business logic]
│   │   └── routers/              [API endpoints]
│   └── tests/                    [Test suite]
│
└── frontend/
    ├── src/
    │   ├── App.jsx               [Main React component]
    │   ├── components/           [UI components]
    │   └── services/api.js       [API client]
    └── public/                   [Static assets]
```

---

## ✅ Implementation Checklist

### What's Been Built

- [x] Smart contract with immutable file registry
- [x] IPFS integration via Pinata
- [x] FastAPI backend with 6 endpoints
- [x] React dashboard with 4 specialized components
- [x] CID-based verification system
- [x] Docker containerization
- [x] Comprehensive test suite
- [x] Production documentation
- [x] Security hardening
- [x] Error handling & logging

### Ready to Deploy

- [x] All code tested & working
- [x] All dependencies specified
- [x] Environment templates created
- [x] Deployment procedures documented
- [x] Security controls in place
- [x] API fully documented
- [x] Frontend polished & responsive

---

## 🚀 Quick Start

### Fastest Path to Running ChainGuard

```bash
# 1. Install dependencies
npm install
cd backend && pip install -r requirements.txt
cd ../contracts && npm install

# 2. Start local chain & deploy contract
npx hardhat node
npx hardhat run scripts/deploy.js --network hardhat

# 3. Configure environment
cp backend/.env.example backend/.env  # Fill in Pinata keys
cp frontend/.env.example frontend/.env

# 4. Start services
docker-compose up

# 5. Open dashboard
# Navigate to http://localhost:5173
```

**Full details in [SETUP_GUIDE.md](./SETUP_GUIDE.md)**

---

## 🎯 Next Steps

1. **Understand the Architecture**: Read this document thoroughly
2. **Follow Setup Guide**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
3. **Deploy Locally**: Run locally first
4. **Test End-to-End**: Verify all workflows
5. **Deploy to Testnet**: Use [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
6. **Go to Production**: When ready to scale

---

**ChainGuard v1.0**  
*Cryptographically Verifiable Content Delivery Network*  
*Built with: Solidity • Python • React • IPFS • Ethereum*

---

*For questions or support, refer to [INDEX.md](./INDEX.md) for navigation or check inline code comments for technical details.*
