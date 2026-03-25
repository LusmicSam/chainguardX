import React from "react";

function VerificationBadge({ status }) {
  const badges = {
    verified: { bg: "#e8f5e9", border: "#4caf50", text: "✅ Verified", color: "#2e7d32" },
    tampered: { bg: "#ffebee", border: "#f44336", text: "⚠️ TAMPERED", color: "#c62828" },
    not_found: { bg: "#fff3e0", border: "#ff9800", text: "❓ Not Found", color: "#e65100" },
    error: { bg: "#fce4ec", border: "#e91e63", text: "❌ Error", color: "#880e4f" },
  };

  const badge = badges[status] || badges.error;

  return (
    <span
      style={{
        display: "inline-block",
        padding: "4px 10px",
        borderRadius: 12,
        fontSize: 12,
        fontWeight: "bold",
        background: badge.bg,
        border: `1px solid ${badge.border}`,
        color: badge.color,
      }}
    >
      {badge.text}
    </span>
  );
}

export default VerificationBadge;
