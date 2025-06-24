import React from "react";

export default function FloatingBackground() {
  return (
    <svg
      style={{
        position: "absolute",
        top: 0, left: 0, width: "100vw", height: "100vh",
        zIndex: 0, pointerEvents: "none"
      }}
      width="100%" height="100%"
    >
      <circle cx="15%" cy="20%" r="80" fill="#373e47" opacity="0.18">
        <animate attributeName="cy" values="20%;30%;20%" dur="12s" repeatCount="indefinite" />
      </circle>
      <circle cx="80%" cy="70%" r="120" fill="#444c56" opacity="0.13">
        <animate attributeName="cx" values="80%;70%;80%" dur="16s" repeatCount="indefinite" />
      </circle>
      <circle cx="60%" cy="10%" r="60" fill="#2d333b" opacity="0.10">
        <animate attributeName="cy" values="10%;18%;10%" dur="10s" repeatCount="indefinite" />
      </circle>
    </svg>
  );
} 