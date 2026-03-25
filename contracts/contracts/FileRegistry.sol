// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title FileRegistry
 * @notice Stores immutable mappings of file names to IPFS CID hashes
 * @dev Used as a tamper-proof ledger for file integrity verification
 */
contract FileRegistry {

    // ============ STATE VARIABLES ============

    address public owner;

    struct FileRecord {
        string cid;
        uint256 timestamp;
        address registeredBy;
        string fileType;
        uint256 fileSize;
        bool exists;
    }

    mapping(string => FileRecord) private fileRecords;
    mapping(string => string[]) private fileHistory;
    string[] private allFileNames;
    mapping(string => bool) private cidExists;
    uint256 public totalFiles;

    // ============ EVENTS ============

    event FileRegistered(
        string indexed fileName,
        string cid,
        uint256 timestamp,
        address indexed registeredBy,
        string fileType,
        uint256 fileSize
    );

    event FileUpdated(
        string indexed fileName,
        string oldCid,
        string newCid,
        uint256 timestamp
    );

    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );

    // ============ MODIFIERS ============

    modifier onlyOwner() {
        require(msg.sender == owner, "FileRegistry: caller is not the owner");
        _;
    }

    modifier nonEmptyString(string memory str) {
        require(bytes(str).length > 0, "FileRegistry: string cannot be empty");
        _;
    }

    // ============ CONSTRUCTOR ============

    constructor() {
        owner = msg.sender;
        emit OwnershipTransferred(address(0), msg.sender);
    }

    // ============ WRITE FUNCTIONS ============

    function registerFile(
        string memory _fileName,
        string memory _cid,
        string memory _fileType,
        uint256 _fileSize
    )
        external
        onlyOwner
        nonEmptyString(_fileName)
        nonEmptyString(_cid)
    {
        require(!cidExists[_cid], "FileRegistry: CID already registered");

        if (fileRecords[_fileName].exists) {
            string memory oldCid = fileRecords[_fileName].cid;
            emit FileUpdated(_fileName, oldCid, _cid, block.timestamp);
        } else {
            allFileNames.push(_fileName);
            totalFiles++;
        }

        fileRecords[_fileName] = FileRecord({
            cid: _cid,
            timestamp: block.timestamp,
            registeredBy: msg.sender,
            fileType: _fileType,
            fileSize: _fileSize,
            exists: true
        });

        fileHistory[_fileName].push(_cid);
        cidExists[_cid] = true;

        emit FileRegistered(
            _fileName,
            _cid,
            block.timestamp,
            msg.sender,
            _fileType,
            _fileSize
        );
    }

    function transferOwnership(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "FileRegistry: new owner is zero address");
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }

    // ============ READ FUNCTIONS ============

    function getFileCID(string memory _fileName)
        external
        view
        returns (string memory cid)
    {
        require(fileRecords[_fileName].exists, "FileRegistry: file not found");
        return fileRecords[_fileName].cid;
    }

    function getFileRecord(string memory _fileName)
        external
        view
        returns (FileRecord memory record)
    {
        require(fileRecords[_fileName].exists, "FileRegistry: file not found");
        return fileRecords[_fileName];
    }

    function verifyFile(string memory _fileName, string memory _cid)
        external
        view
        returns (bool isValid)
    {
        if (!fileRecords[_fileName].exists) {
            return false;
        }
        return keccak256(bytes(fileRecords[_fileName].cid)) == keccak256(bytes(_cid));
    }

    function fileExists(string memory _fileName)
        external
        view
        returns (bool)
    {
        return fileRecords[_fileName].exists;
    }

    function getFileHistory(string memory _fileName)
        external
        view
        returns (string[] memory history)
    {
        return fileHistory[_fileName];
    }

    function getAllFileNames()
        external
        view
        returns (string[] memory names)
    {
        return allFileNames;
    }

    function isCIDRegistered(string memory _cid)
        external
        view
        returns (bool)
    {
        return cidExists[_cid];
    }
}
