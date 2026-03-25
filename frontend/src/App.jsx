/**
 * ChainGuard Dashboard — Main Application Component
 */

import React, { useState, useEffect } from "react";
import FileUpload from "./components/FileUpload";
import FileList from "./components/FileList";
import FileRetrieval from "./components/FileRetrieval";
import VerificationBadge from "./components/VerificationBadge";
import { healthCheck } from "./services/api";
import { Toaster } from "react-hot-toast";

function App() {
  const [health, setHealth] = useState(null);
  const [activeTab, setActiveTab] = useState("upload");
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    healthCheck()
      .then(setHealth)
      .catch(() =>
        setHealth({ status: "offline", pinata_connected: false, blockchain_connected: false })
      );
  }, []);

  const triggerRefresh = () => setRefreshKey((k) => k + 1);

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 20, fontFamily: "monospace" }}>
      <Toaster position="top-right" />

      <h1 style={{ textAlign: "center" }}>🛡️ ChainGuard</h1>
      <p style={{ textAlign: "center", color: "#666" }}>
        Blockchain-Verified File Integrity System
      </p>

      {health && (
        <div
          style={{
            padding: 12,
            marginBottom: 20,
            borderRadius: 8,
            background: health.status === "healthy" ? "#e6ffe6" : "#ffe6e6",
            border: `1px solid ${health.status === "healthy" ? "#00cc00" : "#cc0000"}`,
            textAlign: "center",
          }}
        >
          <strong>System: {health.status.toUpperCase()}</strong>
          {" | "}
          Pinata: {health.pinata_connected ? "✅" : "❌"}
          {" | "}
          Blockchain: {health.blockchain_connected ? "✅" : "❌"}
        </div>
      )}

      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        {["upload", "files", "retrieve"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              flex: 1,
              padding: 12,
              cursor: "pointer",
              border: "2px solid #333",
              borderRadius: 8,
              background: activeTab === tab ? "#333" : "#fff",
              color: activeTab === tab ? "#fff" : "#333",
              fontWeight: "bold",
              fontSize: 14,
              fontFamily: "monospace",
            }}
          >
            {tab === "upload" && "📤 Upload"}
            {tab === "files" && "📋 Registry"}
            {tab === "retrieve" && "🔍 Retrieve & Verify"}
          </button>
        ))}
      </div>

      {activeTab === "upload" && <FileUpload onUploadSuccess={triggerRefresh} />}
      {activeTab === "files" && <FileList key={refreshKey} />}
      {activeTab === "retrieve" && <FileRetrieval />}
    </div>
  );
}

export default App;
