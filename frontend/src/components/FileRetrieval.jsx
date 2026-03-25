import React, { useState } from "react";
import { retrieveFile } from "../services/api";
import VerificationBadge from "./VerificationBadge";
import toast from "react-hot-toast";

function FileRetrieval() {
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRetrieve = async () => {
    if (!fileName.trim()) {
      toast.error("Enter a file name");
      return;
    }
    setLoading(true);
    setResult(null);

    try {
      const data = await retrieveFile(fileName.trim());
      setResult({
        success: true,
        headers: data.headers,
        blobUrl: URL.createObjectURL(data.blob),
        size: data.blob.size,
      });
      toast.success("File retrieved and verified!");
    } catch (err) {
      const status = err.response?.status;
      if (status === 404) {
        setResult({ success: false, error: "File not found in registry" });
      } else if (status === 409) {
        setResult({ success: false, error: "⚠️ TAMPERING DETECTED!", tampered: true });
        toast.error("INTEGRITY VIOLATION DETECTED!");
      } else {
        setResult({ success: false, error: err.message });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>🔍 Retrieve & Verify File</h2>

      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        <input
          type="text"
          value={fileName}
          onChange={(e) => setFileName(e.target.value)}
          placeholder="Enter file name (e.g., report.pdf)"
          onKeyDown={(e) => e.key === "Enter" && handleRetrieve()}
          style={{
            flex: 1, padding: 12, fontSize: 14, border: "2px solid #ddd",
            borderRadius: 8, fontFamily: "monospace",
          }}
        />
        <button
          onClick={handleRetrieve}
          disabled={loading}
          style={{
            padding: "12px 24px", fontSize: 14, cursor: "pointer",
            background: "#333", color: "#fff", border: "none",
            borderRadius: 8, fontFamily: "monospace",
          }}
        >
          {loading ? "⏳ Verifying..." : "🔍 Retrieve"}
        </button>
      </div>

      {result && result.success && (
        <div style={{
          padding: 16, background: "#e8f5e9", border: "1px solid #4caf50", borderRadius: 8,
        }}>
          <h3>
            <VerificationBadge status={result.headers.status} />
            {" "}File Retrieved Successfully
          </h3>
          <table style={{ width: "100%", fontSize: 13 }}>
            <tbody>
              <tr><td><strong>Status:</strong></td><td>{result.headers.status}</td></tr>
              <tr><td><strong>CID:</strong></td><td style={{wordBreak:"break-all"}}>{result.headers.cid}</td></tr>
              <tr><td><strong>Blockchain Verified:</strong></td><td>{result.headers.verified}</td></tr>
              <tr><td><strong>Registered By:</strong></td><td style={{wordBreak:"break-all"}}>{result.headers.registeredBy}</td></tr>
              <tr><td><strong>Size:</strong></td><td>{result.size} bytes</td></tr>
            </tbody>
          </table>
          <a href={result.blobUrl} download={fileName} style={{
            display: "inline-block", marginTop: 12, padding: "8px 16px",
            background: "#2e7d32", color: "#fff", textDecoration: "none", borderRadius: 6,
          }}>
            📥 Download Verified File
          </a>
        </div>
      )}

      {result && !result.success && (
        <div style={{
          padding: 16, borderRadius: 8,
          background: result.tampered ? "#ffebee" : "#fff3e0",
          border: `1px solid ${result.tampered ? "#f44336" : "#ff9800"}`,
        }}>
          <h3>{result.tampered ? "🚨 INTEGRITY VIOLATION" : "⚠️ Error"}</h3>
          <p>{result.error}</p>
          {result.tampered && (
            <p style={{ color: "#c62828", fontWeight: "bold" }}>
              The file content does not match the blockchain record.
              This file may have been tampered with!
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default FileRetrieval;
