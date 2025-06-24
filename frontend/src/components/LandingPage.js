import React from "react";

function GlassShapes() {
  return (
    <div style={{ position: "absolute", inset: 0, zIndex: 0, pointerEvents: "none" }}>
      <div style={{
        position: "absolute", left: "10%", top: "10%", width: 220, height: 220,
        background: "#b3d1f7", filter: "blur(80px)", opacity: 0.45, borderRadius: "50%"
      }} />
      <div style={{
        position: "absolute", right: "8%", top: "30%", width: 180, height: 180,
        background: "#cbe5ff", filter: "blur(70px)", opacity: 0.38, borderRadius: "40% 60% 60% 40% / 60% 40% 60% 40%"
      }} />
      <div style={{
        position: "absolute", left: "20%", bottom: "8%", width: 260, height: 120,
        background: "#a0c4f6", filter: "blur(90px)", opacity: 0.32, borderRadius: "60% 40% 40% 60% / 40% 60% 60% 40%"
      }} />
      <div style={{
        position: "absolute", right: "18%", bottom: "10%", width: 140, height: 140,
        background: "#b3d1f7", filter: "blur(60px)", opacity: 0.30, borderRadius: "50%"
      }} />
    </div>
  );
}

export default function LandingPage({ onStart }) {
  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100vw",
        background: "radial-gradient(ellipse at center, #cbe5ff 0%, #b3d1f7 60%, #a0c4f6 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        overflow: "hidden",
        fontFamily: "Inter, system-ui, sans-serif"
      }}
    >
      <GlassShapes />
      <div
        style={{
          position: "relative",
          width: "75vw",
          maxWidth: 1100,
          margin: "60px auto 0 auto",
          background: "rgba(255,255,255,0.18)",
          border: "1.5px solid rgba(60,80,120,0.18)",
          borderRadius: 32,
          boxShadow: "0 8px 64px 0 rgba(60,80,120,0.18), 0 0 0 4px rgba(60,80,120,0.10)",
          padding: 36,
          color: "#222",
          zIndex: 1,
          textAlign: "center",
          fontFamily: "Inter, system-ui, sans-serif"
        }}
      >
        <h1
          style={{
            fontSize: "5.2rem",
            fontWeight: 700,
            color: "#222",
            marginBottom: 24,
            lineHeight: 1.1,
            fontFamily: "Inter, system-ui, sans-serif"
          }}
        >
          DataPilot.<br />
        </h1>
        <div
          style={{
            fontSize: "2.00rem",
            color: "#444",
            marginBottom: 40,
            fontWeight: 400,
            fontFamily: "Inter, system-ui, sans-serif"
          }}
        >
            Your autopilot for data science
        </div>
        <div
          style={{
            fontSize: "1.25rem",
            color: "#444",
            marginBottom: 40,
            fontWeight: 400,
            fontFamily: "Inter, system-ui, sans-serif"
          }}
        >
           Data Pilot is your intelligent assistant for data science.<br/>
          Just upload a CSV file — from Kaggle or anywhere — and let our agentic AI system take over....
        </div>
        <button
          onClick={onStart}
          style={{
            background: "#222",
            color: "#fff",
            fontSize: "1.2rem",
            border: "none",
            borderRadius: 32,
            padding: "18px 48px",
            fontWeight: 600,
            boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
            cursor: "pointer",
            transition: "background 0.2s",
            fontFamily: "Inter, system-ui, sans-serif"
          }}
        >
          Get Started
        </button>
      </div>
    </div>
  );
} 