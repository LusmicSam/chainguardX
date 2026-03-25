const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FileRegistry", function () {
  let fileRegistry;
  let owner;
  let addr1;
  let addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    const FileRegistry = await ethers.getContractFactory("FileRegistry");
    fileRegistry = await FileRegistry.deploy();
    await fileRegistry.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await fileRegistry.owner()).to.equal(owner.address);
    });

    it("Should start with zero total files", async function () {
      expect(await fileRegistry.totalFiles()).to.equal(0);
    });
  });

  describe("File Registration", function () {
    const fileName = "test_image.png";
    const cid = "QmTest1234567890abcdefghijklmnopqrstuvwxyz12";
    const fileType = "image/png";
    const fileSize = 1024;

    it("Should register a new file", async function () {
      await expect(
        fileRegistry.registerFile(fileName, cid, fileType, fileSize)
      ).to.emit(fileRegistry, "FileRegistered");

      expect(await fileRegistry.totalFiles()).to.equal(1);
    });

    it("Should retrieve correct CID for registered file", async function () {
      await fileRegistry.registerFile(fileName, cid, fileType, fileSize);
      expect(await fileRegistry.getFileCID(fileName)).to.equal(cid);
    });

    it("Should verify correct CID returns true", async function () {
      await fileRegistry.registerFile(fileName, cid, fileType, fileSize);
      expect(await fileRegistry.verifyFile(fileName, cid)).to.equal(true);
    });

    it("Should verify incorrect CID returns false", async function () {
      await fileRegistry.registerFile(fileName, cid, fileType, fileSize);
      expect(
        await fileRegistry.verifyFile(fileName, "QmFakeCID123")
      ).to.equal(false);
    });

    it("Should reject registration from non-owner", async function () {
      await expect(
        fileRegistry
          .connect(addr1)
          .registerFile(fileName, cid, fileType, fileSize)
      ).to.be.revertedWith("FileRegistry: caller is not the owner");
    });

    it("Should reject empty file name", async function () {
      await expect(
        fileRegistry.registerFile("", cid, fileType, fileSize)
      ).to.be.revertedWith("FileRegistry: string cannot be empty");
    });

    it("Should reject duplicate CID", async function () {
      await fileRegistry.registerFile(fileName, cid, fileType, fileSize);
      await expect(
        fileRegistry.registerFile("another_file.png", cid, fileType, fileSize)
      ).to.be.revertedWith("FileRegistry: CID already registered");
    });

    it("Should maintain file history on update", async function () {
      const cid2 = "QmUpdatedCID567890abcdefghijklmnopqrstuvwx";
      await fileRegistry.registerFile(fileName, cid, fileType, fileSize);
      await fileRegistry.registerFile(fileName, cid2, fileType, fileSize);

      const history = await fileRegistry.getFileHistory(fileName);
      expect(history.length).to.equal(2);
      expect(history[0]).to.equal(cid);
      expect(history[1]).to.equal(cid2);
    });

    it("Should list all file names", async function () {
      await fileRegistry.registerFile("file1.png", cid, fileType, fileSize);
      const cid2 = "QmAnotherCID567890abcdefghijklmnopqrstuvwxy";
      await fileRegistry.registerFile(
        "file2.pdf",
        cid2,
        "application/pdf",
        2048
      );

      const names = await fileRegistry.getAllFileNames();
      expect(names.length).to.equal(2);
      expect(names).to.include("file1.png");
      expect(names).to.include("file2.pdf");
    });
  });

  describe("Ownership", function () {
    it("Should transfer ownership", async function () {
      await fileRegistry.transferOwnership(addr1.address);
      expect(await fileRegistry.owner()).to.equal(addr1.address);
    });

    it("Should reject transfer to zero address", async function () {
      await expect(
        fileRegistry.transferOwnership(ethers.ZeroAddress)
      ).to.be.revertedWith("FileRegistry: new owner is zero address");
    });
  });
});
