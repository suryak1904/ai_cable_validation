"use client";

import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const validate = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setData(null);
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/design/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        throw new Error("Validation service error");
      }

      const json = await res.json();
      setData(json);
    } catch (e) {
      setError("Unable to validate cable specification.");
    } finally {
      setLoading(false);
    }
  };

  const statusColor = (s: string) =>
    s === "PASS" ? "#2e7d32" : s === "FAIL" ? "#d32f2f" : "#ed6c02";

  const renderValue = (value: any) => {
    if (typeof value === "object") {
      return (
        <pre
          style={{
            background: "#f7f7f7",
            padding: 12,
            borderRadius: 6,
            fontSize: 13,
            overflowX: "auto",
          }}
        >
          {JSON.stringify(value, null, 2)}
        </pre>
      );
    }
    return <span>{String(value)}</span>;
  };

  return (
    <main
      style={{
        backgroundColor: "#ffffff",
        color: "#000000",
        minHeight: "100vh",
        padding: 40,
        maxWidth: 900,
        margin: "0 auto",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h2 style={{ marginBottom: 20 }}>Cable Validation (IEC_60502)</h2>
      <textarea
        rows={4}
        placeholder="Enter cable specification..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{
          width: "100%",
          padding: 12,
          border: "2px solid #1976d2",
          borderRadius: 6,
          color: "#000000",
          backgroundColor: "#ffffff",
          outline: "none",
          fontSize: 14,
        }}
      />
      <button
        onClick={validate}
        disabled={loading}
        style={{
          marginTop: 14,
          padding: "10px 18px",
          backgroundColor: "#1976d2",
          color: "#ffffff",
          border: "none",
          borderRadius: 6,
          cursor: "pointer",
          fontSize: 14,
        }}
      >
        {loading ? "Validating..." : "Validate"}
      </button>
      {loading && (
        <p style={{ marginTop: 12, fontStyle: "italic" }}>
          Processing validation…
        </p>
      )}
      {error && (
        <p style={{ marginTop: 12, color: "#d32f2f" }}>{error}</p>
      )}

      {data && (
        <div style={{ marginTop: 30 }}>
          {typeof data.overall_status === "string" && (
            <div
              style={{
                padding: 12,
                borderRadius: 6,
                backgroundColor: "#f5f5f5",
                marginBottom: 20,
                fontWeight: "bold",
                color: statusColor(data.overall_status),
              }}
            >
              Overall Status: {data.overall_status}
            </div>
          )}

          <h4>Validation Output</h4>

          {Object.entries(data).map(([key, value]) => (
            <div
              key={key}
              style={{
                border: "1px solid #ddd",
                borderRadius: 6,
                padding: 12,
                marginBottom: 12,
              }}
            >
              <strong>{key}</strong>
              <div style={{ marginTop: 6 }}>{renderValue(value)}</div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
