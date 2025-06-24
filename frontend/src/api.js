const API_BASE = "http://localhost:8000";

export async function uploadAndRun(file) {
  const formData = new FormData();
  formData.append("file", file);
  // Upload
  const uploadRes = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });
  if (!uploadRes.ok) throw new Error("Upload failed");
  const { file_id } = await uploadRes.json();
  console.log("file_id: ", file_id);
  // Run
  const runRes = await fetch(`${API_BASE}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ file_id }),
  });
  if (!runRes.ok) throw new Error("Pipeline run failed");
  return runRes.json();
}

export async function fetchFile(path) {
  const res = await fetch(`http://localhost:8000/${path}`);
  if (!res.ok) throw new Error("Failed to fetch file");
  return res.text();
} 