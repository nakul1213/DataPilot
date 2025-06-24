import React, { useState } from "react";
import NotebookPreview from "./NotebookPreview";

export default function PipelineTabs({ notebook, readme, onDownload, darkMode }) {
  const [tab, setTab] = useState("notebook");

  const bg = darkMode ? "#22272e" : "#fff";
  const border = darkMode ? "#373e47" : "#e1e4e8";
  const tabBg = darkMode ? "#2d333b" : "#f6f8fa";
  const activeBg = darkMode ? "#22272e" : "#fff";
  const text = darkMode ? "#adbac7" : "#24292f";
  const btnBg = darkMode ? "#347d39" : "#2ea44f";

  return (
    <div style={{ marginTop: 24 }}>
      <div style={{
        display: "flex",
        borderBottom: `1px solid ${border}`,
        background: tabBg
      }}>
        <button
          style={{
            flex: 1,
            padding: "12px 0",
            border: "none",
            background: tab === "notebook" ? activeBg : "transparent",
            fontWeight: tab === "notebook" ? "bold" : "normal",
            color: text,
            cursor: "pointer"
          }}
          onClick={() => setTab("notebook")}
        >
          Notebook
        </button>
        <button
          style={{
            flex: 1,
            padding: "12px 0",
            border: "none",
            background: tab === "readme" ? activeBg : "transparent",
            fontWeight: tab === "readme" ? "bold" : "normal",
            color: text,
            cursor: "pointer"
          }}
          onClick={() => setTab("readme")}
        >
          README
        </button>
      </div>
      <div style={{
        background: bg,
        border: `1px solid ${border}`,
        borderTop: "none",
        minHeight: 200,
        padding: 16,
        fontFamily: "monospace",
        whiteSpace: "pre-wrap",
        overflowX: "auto",
        color: text
      }}>
        {tab === "notebook"
          ? <NotebookPreview notebookJSON={notebook} />
          : <div style={{ whiteSpace: "pre-wrap" }}>{readme}</div>
        }
      </div>
      <div style={{ marginTop: 12, textAlign: "right" }}>
        <button
          style={{
            marginRight: 8,
            background: btnBg,
            color: "#fff",
            border: "none",
            padding: "8px 16px",
            borderRadius: 6,
            cursor: "pointer"
          }}
          onClick={() => onDownload(tab)}
        >
          Download {tab === "notebook" ? "Notebook" : "README"}
        </button>
      </div>
    </div>
  );
} 