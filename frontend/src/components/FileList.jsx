import React, { useState, useEffect } from "react";
import { listFiles, verifyFile } from "../services/api";
import VerificationBadge from "./VerificationBadge";
import toast from "react-hot-toast";

function FileList() {
  const [registry, setRegistry] = useState(null);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState({});

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const data = await listFiles();
      setRegistry(data);
    } catch (err) {
      toast.error("Failed to load registry");
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (fileName) => {
    setVerifying((v) => ({ ...v, [fileName]: "loading" }));
    try {
      const result = await verifyFile(fileName);
      setVerifying((v) => ({ ...v, [fileName]: result.status }));
    } catch {
      setVerifying((v) => ({ ...v, [fileName]: "error" }));
    }
  };

  if (loading) return <p>Loading registry...</p>;
  if (!registry || registry.files.length === 0)
    return <p>No files registered yet. Upload a file first.</p>;

  return (
    <div>
      <h2>📋 File Registry ({registry.total_files} files)</h2>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
        <thead>
          <tr style={{ background: "#f5f5f5" }}>
            <th style={thStyle}>Name</th>
            <th style={thStyle}>CID</th>
            <th style={thStyle}>Type</th>
            <th style={thStyle}>Size</th>
            <th style={thStyle}>Status</th>
          </tr>
        </thead>
        <tbody>
          {registry.files.map((file) => (
            <tr key={file.file_name} style={{ borderBottom: "1px solid #eee" }}>
              <td style={tdStyle}>{file.file_name}</td>
              <td style={{ ...tdStyle, maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis" }}>
                {file.cid}
              </td>
              <td style={tdStyle}>{file.file_type}</td>
              <td style={tdStyle}>{file.file_size}B</td>
              <td style={tdStyle}>
                {verifying[file.file_name] === "loading" ? (
                  "⏳..."
                ) : verifying[file.file_name] ? (
                  <VerificationBadge status={verifying[file.file_name]} />
                ) : (
                  <button
                    onClick={() => handleVerify(file.file_name)}
                    style={{ cursor: "pointer", padding: "4px 8px", fontSize: 12 }}
                  >
                    Verify
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const thStyle = { textAlign: "left", padding: 8, borderBottom: "2px solid #ddd" };
const tdStyle = { padding: 8 };

export default FileList;
