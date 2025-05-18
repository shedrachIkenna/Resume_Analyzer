import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please upload a file first");

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data);
    } catch (err) {
      console.error("Upload error:", err);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

const handleDownload = async () => {
  if (!file) {
    alert("Please upload a resume first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:8000/download", {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    alert("Failed to download report.");
    return;
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", "resume_report.pdf");
  document.body.appendChild(link);
  link.click();
  link.remove();
};

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Smart Resume Analyzer</h1>

      <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: "1rem" }}>
        Upload & Analyze
      </button>

      <button
        onClick={handleDownload}
        disabled={!file}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition disabled:opacity-50 ml-10"
      >
        Download Report as PDF
      </button>

      {loading && <p>⏳ Analyzing resume, please wait...</p>}

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Analysis Result</h2>
          <ul>
            <li><strong>Name:</strong> {result.name}</li>
            <li><strong>Email:</strong> {result.email || "Not found"}</li>
            <li><strong>Phone:</strong> {result.phone}</li>
            <li><strong>Skills:</strong> {result.skills.join(", ")}</li>
            <li><strong>Predicted Roles:</strong> {result.predicted_roles.join(", ")}</li>
          </ul>
          <h3>Education</h3>
          <ul>
            {result.education.map((edu, i) => (
              <li key={i}>{edu}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
