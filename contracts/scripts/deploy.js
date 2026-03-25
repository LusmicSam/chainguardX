const hre = require("hardhat");

async function main() {
  console.log("=".repeat(60));
  console.log("DEPLOYING FileRegistry CONTRACT");
  console.log("=".repeat(60));

  const [deployer] = await hre.ethers.getSigners();
  console.log(`\nDeployer address: ${deployer.address}`);

  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log(`Deployer balance: ${hre.ethers.formatEther(balance)} ETH`);

  if (balance === 0n) {
    throw new Error("Deployer has no ETH. Get testnet ETH from a faucet.");
  }

  console.log("\nDeploying contract...");
  const FileRegistry = await hre.ethers.getContractFactory("FileRegistry");
  const fileRegistry = await FileRegistry.deploy();

  await fileRegistry.waitForDeployment();

  const contractAddress = await fileRegistry.getAddress();
  console.log(`\n✅ FileRegistry deployed to: ${contractAddress}`);
  console.log(`   Network: ${hre.network.name}`);
  console.log(`   Chain ID: ${(await hre.ethers.provider.getNetwork()).chainId}`);

  const owner = await fileRegistry.owner();
  console.log(`   Owner: ${owner}`);

  console.log("\n" + "=".repeat(60));
  console.log("ADD THESE TO YOUR BACKEND .env FILE:");
  console.log("=".repeat(60));
  console.log(`CONTRACT_ADDRESS=${contractAddress}`);
  console.log(`BLOCKCHAIN_NETWORK=${hre.network.name}`);
  console.log("=".repeat(60));

  if (hre.network.name === "sepolia") {
    console.log("\nWaiting for 5 block confirmations...");
    const deployTx = fileRegistry.deploymentTransaction();
    await deployTx.wait(5);

    console.log("Verifying contract on Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [],
      });
      console.log("✅ Contract verified on Etherscan!");
    } catch (error) {
      console.log("⚠️  Etherscan verification failed:", error.message);
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
