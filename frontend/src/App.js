import React, { useRef, useState } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { uploadAndRun, fetchFile } from "./api";
import PipelineTabs from "./components/PipelineTabs";
import LandingPage from "./components/LandingPage";

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

function FadeWrapper({ children }) {
  const location = useLocation();
  const [show, setShow] = useState(false);
  React.useEffect(() => {
    setShow(false);
    const timeout = setTimeout(() => setShow(true), 10);
    return () => clearTimeout(timeout);
  }, [location.pathname]);
  return (
    <div style={{
      transition: "opacity 0.5s cubic-bezier(.4,0,.2,1)",
      opacity: show ? 1 : 0,
      minHeight: "100vh"
    }}>
      {children}
    </div>
  );
}

function MainPage() {
  const fileInput = useRef();
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("Idle");
  const [notebook, setNotebook] = useState("");
  const [readme, setReadme] = useState("");
  const [notebookPath, setNotebookPath] = useState("");
  const [readmePath, setReadmePath] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setNotebook("");
    setReadme("");
    setStatus("Idle");
  };

  const handleRemoveFile = () => {
    setFile(null);
    setNotebook("");
    setReadme("");
    setStatus("Idle");
    if (fileInput.current) fileInput.current.value = "";
  };

  const handleUploadAndRun = async () => {
    setStatus("Processing...");
    try {
      const res = await uploadAndRun(file);
      setNotebookPath(res.notebook);
      setReadmePath(res.readme);
      const [nb, rd] = await Promise.all([
        fetchFile(res.notebook),
        fetchFile(res.readme),
      ]);
      setNotebook(nb);
      setReadme(rd);
      setStatus("Done!");
    } catch (err) {
      setStatus("Error: " + err.message);
    }
  };

  const handleDownload = (type) => {
    const path = type === "notebook" ? notebookPath : readmePath;
    window.open(`http://localhost:8000/${path}`, "_blank");
  };

  return (
    <div style={{
      position: "relative",
      minHeight: "100vh",
      background: "radial-gradient(ellipse at center, #cbe5ff 0%, #b3d1f7 60%, #a0c4f6 100%)",
      overflow: "hidden",
      fontFamily: "Inter, system-ui, sans-serif"
    }}>
      <GlassShapes />
      <div style={{
        width: "75vw",
        maxWidth: 1100,
        margin: "60px auto 0 auto",
        background: "rgba(255,255,255,0.18)",
        border: "1.5px solid rgba(60,80,120,0.18)",
        borderRadius: 32,
        boxShadow: "0 8px 64px 0 rgba(60,80,120,0.18), 0 0 0 4px rgba(60,80,120,0.10)",
        padding: 36,
        color: "#222",
        position: "relative",
        zIndex: 1,
        textAlign: "center",
        fontFamily: "Inter, system-ui, sans-serif"
      }}>
        <div style={{ fontSize: 50, color: "#222", fontWeight: 700, letterSpacing: 2, marginBottom: 8, fontFamily: "Inter, system-ui, sans-serif" }}>
           DataPilot.
        </div>
        <div style={{ fontSize: 26, fontWeight: 600, color: "#222", marginBottom: 10, letterSpacing: 0.5, fontFamily: "Inter, system-ui, sans-serif" }}>
          Upload your CSV and get a ready-to-use Jupyter notebook in seconds.
        </div>
        <div style={{ fontSize: 17, color: "#444", marginBottom: 32, fontWeight: 400, fontFamily: "Inter, system-ui, sans-serif" }}>
          1. Click <b>Choose CSV File</b> to select your data.<br />
          2. Click <b>Upload & Run</b> to generate your notebook and README.<br />
          3. Preview or download your results instantly.
        </div>
        <input
          type="file"
          accept=".csv"
          ref={fileInput}
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
        {!file && (
          <button
            onClick={() => fileInput.current.click()}
            style={{
              background: "#347d39",
              color: "#fff",
              border: "none",
              padding: "16px 40px",
              borderRadius: 24,
              fontWeight: 600,
              cursor: "pointer",
              fontSize: 18,
              margin: "0 auto",
              display: "block",
              marginBottom: 24
            }}
          >
            Choose CSV File
          </button>
        )}
        {file && (
          <>
            <div style={{ fontSize: 20, color: "#222", fontWeight: 500, marginBottom: 18, marginTop: 8, fontFamily: "Inter, system-ui, sans-serif" }}>{file.name}</div>
            <div style={{ display: "flex", justifyContent: "center", gap: 24, marginBottom: 24 }}>
              <button
                onClick={handleUploadAndRun}
                style={{
                  background: "#347d39",
                  color: "#fff",
                  border: "none",
                  padding: "16px 40px",
                  borderRadius: 24,
                  fontWeight: 600,
                  cursor: "pointer",
                  fontSize: 18,
                  minWidth: 160
                }}
              >
                Upload & Run
              </button>
              <button
                onClick={handleRemoveFile}
                style={{
                  background: "#f44336",
                  color: "#fff",
                  border: "none",
                  padding: "16px 40px",
                  borderRadius: 24,
                  fontWeight: 600,
                  cursor: "pointer",
                  fontSize: 18,
                  minWidth: 160
                }}
                title="Remove file"
              >
                Remove
              </button>
            </div>
          </>
        )}
        <div style={{ marginBottom: 16, color: status.startsWith("Error") ? "#f47067" : "#347d39", fontWeight: 500, fontSize: 16 }}>{status}</div>
        {(notebook || readme) && (
          <PipelineTabs
            notebook={notebook}
            readme={readme}
            onDownload={handleDownload}
            darkMode={false}
          />
        )}
      </div>
    </div>
  );
}

export default function App() {
  const navigate = useNavigate();
  return (
    <FadeWrapper>
      <Routes>
        <Route path="/" element={<LandingPage onStart={() => navigate('/upandrun')} />} />
        <Route path="/upandrun" element={<MainPage />} />
      </Routes>
    </FadeWrapper>
  );
} 