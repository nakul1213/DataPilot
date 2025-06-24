import React from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function NotebookPreview({ notebookJSON }) {
  let cells = [];
  try {
    const nb = JSON.parse(notebookJSON);
    cells = nb.cells.filter(cell => cell.cell_type === "code").slice(0, 3);
  } catch {
    return <div>Invalid notebook format.</div>;
  }

  // Always use dark theme
  const cellBg = "#22272e";
  const cellHeaderBg = "#2d333b";
  const cellHeaderColor = "#adbac7";

  return (
    <div>
      {cells.map((cell, idx) => (
        <div
          key={idx}
          style={{
            border: `1px solid #373e47`,
            borderRadius: 6,
            marginBottom: 16,
            background: cellBg,
            padding: 0,
            overflow: "hidden"
          }}
        >
          <div style={{
            background: cellHeaderBg,
            padding: "4px 12px",
            fontFamily: "monospace",
            color: cellHeaderColor
          }}>
            In [{cell.execution_count || " "}]:
          </div>
          <SyntaxHighlighter
            language="python"
            style={vscDarkPlus}
            customStyle={{ margin: 0, padding: 12, background: cellBg, color: cellHeaderColor }}
          >
            {cell.source.join("")}
          </SyntaxHighlighter>
        </div>
      ))}
    </div>
  );
} 