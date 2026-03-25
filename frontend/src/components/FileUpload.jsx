import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { uploadFile } from "../services/api";
import toast from "react-hot-toast";

function FileUpload({ onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  const onDrop = useCallback(
    async (acceptedFiles) => {
      if (acceptedFiles.length === 0) return;
      const file = acceptedFiles[0];

      setUploading(true);
      setResult(null);

      try {
        const res = await uploadFile(file);
        setResult(res);
        toast.success(`File registered on blockchain!`);
        onUploadSuccess?.();
      } catch (err) {
        const msg = err.response?.data?.detail || err.message;
        toast.error(`Upload failed: ${msg}`);
      } finally {
        setUploading(false);
      }
    },
    [onUploadSuccess]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    maxSize: 50 * 1024 * 1024,
  });

  return (
    <div>
      <h2>📤 Upload File</h2>

      <div
        {...getRootProps()}
        style={{
          border: "3px dashed #999",
          borderRadius: 12,
          padding: 40,
          textAlign: "center",
          cursor: "pointer",
          background: isDragActive ? "#e3f2fd" : "#fafafa",
          transition: "background 0.2s",
        }}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <div>
            <p style={{ fontSize: 24 }}>⏳</p>
            <p>Uploading to IPFS & registering on blockchain...</p>
            <p style={{ color: "#999", fontSize: 12 }}>This may take 15-30 seconds</p>
          </div>
        ) : isDragActive ? (
          <p>Drop the file here...</p>
        ) : (
          <div>
            <p style={{ fontSize: 24 }}>📁</p>
            <p>Drag & drop a file here, or click to select</p>
            <p style={{ color: "#999", fontSize: 12 }}>Max 50MB</p>
          </div>
        )}
      </div>

      {result && (
        <div
          style={{
            marginTop: 20,
            padding: 16,
            background: "#e8f5e9",
            border: "1px solid #4caf50",
            borderRadius: 8,
            fontSize: 13,
          }}
        >
          <h3 style={{ color: "#2e7d32" }}>✅ Upload Successful</h3>
          <table style={{ width: "100%" }}>
            <tbody>
              <tr><td><strong>File:</strong></td><td>{result.file_name}</td></tr>
              <tr><td><strong>IPFS CID:</strong></td><td style={{wordBreak:"break-all"}}>{result.ipfs_cid}</td></tr>
              <tr><td><strong>TX Hash:</strong></td><td style={{wordBreak:"break-all"}}>{result.transaction_hash}</td></tr>
              <tr><td><strong>Block:</strong></td><td>{result.block_number}</td></tr>
              <tr><td><strong>Size:</strong></td><td>{result.file_size} bytes</td></tr>
              <tr>
                <td><strong>IPFS URL:</strong></td>
                <td>
                  <a href={result.ipfs_url} target="_blank" rel="noreferrer">
                    View on IPFS ↗
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
