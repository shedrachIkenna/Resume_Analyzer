import { useState, useEffect } from "react";
import axios from "axios";
import DebugPanel from "./DebugPanel"; // Import the debug panel

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));
  const [showRegister, setShowRegister] = useState(false);

  // Login states
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // Registration states
  const [regUsername, setRegUsername] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regFullName, setRegFullName] = useState("");

  // Set up axios interceptor for authentication errors
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      response => response,
      error => {
        if (error.response && error.response.status === 401) {
          // Handle token expiration
          setToken(null);
          setIsLoggedIn(false);
          localStorage.removeItem("token");
          alert("Your session has expired. Please login again.");
        }
        return Promise.reject(error);
      }
    );

    return () => {
      // Clean up interceptor when component unmounts
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  // Set axios default auth header when token changes
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common["Authorization"];
    }
  }, [token]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleLogin = async () => {
    try {
      // OAuth2 expects form data, not JSON
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);
      
      const response = await axios.post("http://localhost:8000/token", params);

      const accessToken = response.data.access_token;
      
      // Save token to localStorage and state
      localStorage.setItem("token", accessToken);
      setToken(accessToken);
      setIsLoggedIn(true);
      
      // Clear login form
      setUsername("");
      setPassword("");
      
      alert("Login successful!");
    } catch (error) {
      alert("Login failed: " + (error.response?.data?.detail || "Unknown error"));
      console.error("Login error:", error);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Please upload a file first");
    if (!token) return alert("Please login first");

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/predict", formData, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
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
    if (!token) return alert("Please login first");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/download", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        if (response.status === 401) {
          setToken(null);
          setIsLoggedIn(false);
          localStorage.removeItem("token");
          alert("Your session has expired. Please login again.");
          return;
        }
        alert("Failed to download report.");
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "resume_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      alert("Error downloading report");
      console.error(err);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setIsLoggedIn(false);
    localStorage.removeItem("token");
    setResult(null);
  };

  const handleRegister = async () => {
    if (!regUsername || !regPassword) {
      alert("Username and password are required");
      return;
    }

    try {
      // Create the registration data object
      const userData = {
        username: regUsername,
        password: regPassword,
      };
      
      // Only add optional fields if they have values
      if (regEmail) userData.email = regEmail;
      if (regFullName) userData.full_name = regFullName;
      
      console.log("Sending registration data:", userData);
      
      const response = await axios.post("http://localhost:8000/register", userData);

      console.log("Registration response:", response.data);
      alert("Registration successful! Please login.");
      setShowRegister(false);
      // Pre-fill login form with registered username
      setUsername(regUsername);
      
      // Clear registration form
      setRegUsername("");
      setRegPassword("");
      setRegEmail("");
      setRegFullName("");
    } catch (error) {
      console.error("Registration error:", error);
      alert("Registration failed: " + (error.response?.data?.detail || JSON.stringify(error.response?.data) || "Unknown error"));
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Smart Resume Analyzer</h1>

      {/* Authentication Section */}
      {isLoggedIn ? (
        <div style={{ marginBottom: "1rem" }}>
          <p>You are logged in</p>
          <button 
            onClick={handleLogout}
            style={{ backgroundColor: "#f44336", color: "white", padding: "0.5rem 1rem", border: "none", borderRadius: "4px", cursor: "pointer" }}
          >
            Logout
          </button>
        </div>
      ) : (
        <div style={{ marginBottom: "1rem" }}>
          {showRegister ? (
            <div style={{ backgroundColor: "#f8f9fa", padding: "1rem", borderRadius: "8px", marginBottom: "1rem" }}>
              <h3>Register</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem", maxWidth: "300px" }}>
                <input
                  style={{ padding: "0.5rem" }}
                  placeholder="Username*"
                  value={regUsername}
                  onChange={(e) => setRegUsername(e.target.value)}
                />
                <input
                  style={{ padding: "0.5rem" }}
                  type="password"
                  placeholder="Password*"
                  value={regPassword}
                  onChange={(e) => setRegPassword(e.target.value)}
                />
                <input
                  style={{ padding: "0.5rem" }}
                  type="email"
                  placeholder="Email (optional)"
                  value={regEmail}
                  onChange={(e) => setRegEmail(e.target.value)}
                />
                <input
                  style={{ padding: "0.5rem" }}
                  placeholder="Full Name (optional)"
                  value={regFullName}
                  onChange={(e) => setRegFullName(e.target.value)}
                />
                <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.5rem" }}>
                  <button 
                    onClick={handleRegister}
                    style={{ backgroundColor: "#4CAF50", color: "white", padding: "0.5rem 1rem", border: "none", borderRadius: "4px", cursor: "pointer", flex: 1 }}
                  >
                    Register
                  </button>
                  <button 
                    onClick={() => setShowRegister(false)}
                    style={{ backgroundColor: "#6c757d", color: "white", padding: "0.5rem 1rem", border: "none", borderRadius: "4px", cursor: "pointer", flex: 1 }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div>
              <input
                style={{ padding: "0.5rem", marginRight: "0.5rem" }}
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                style={{ padding: "0.5rem", marginRight: "0.5rem" }}
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button 
                onClick={handleLogin}
                style={{ backgroundColor: "#4CAF50", color: "white", padding: "0.5rem 1rem", border: "none", borderRadius: "4px", cursor: "pointer", marginRight: "0.5rem" }}
              >
                Login
              </button>
              <button 
                onClick={() => setShowRegister(true)}
                style={{ backgroundColor: "#0275d8", color: "white", padding: "0.5rem 1rem", border: "none", borderRadius: "4px", cursor: "pointer" }}
              >
                Sign Up
              </button>
            </div>
          )}
        </div>
      )}

      {/* File Upload Section */}
      <div style={{ marginTop: "1rem" }}>
        <input 
          type="file" 
          accept=".pdf,.docx" 
          onChange={handleFileChange} 
          style={{ marginRight: "1rem" }}
        />
        <button 
          onClick={handleUpload} 
          disabled={!isLoggedIn || !file}
          style={{ 
            backgroundColor: "#2196F3", 
            color: "white", 
            padding: "0.5rem 1rem", 
            border: "none", 
            borderRadius: "4px", 
            cursor: isLoggedIn && file ? "pointer" : "not-allowed",
            opacity: isLoggedIn && file ? 1 : 0.7
          }}
        >
          Upload & Analyze
        </button>

        <button
          onClick={handleDownload}
          disabled={!isLoggedIn || !file || !result}
          style={{ 
            backgroundColor: "#4CAF50", 
            color: "white", 
            padding: "0.5rem 1rem", 
            border: "none", 
            borderRadius: "4px", 
            marginLeft: "1rem",
            cursor: isLoggedIn && file && result ? "pointer" : "not-allowed",
            opacity: isLoggedIn && file && result ? 1 : 0.7
          }}
        >
          Download Report as PDF
        </button>
      </div>

      {loading && <p style={{ margin: "1rem 0" }}>⏳ Analyzing resume, please wait...</p>}

      {/* Debug Panel - Remove in production */}
      <DebugPanel />

      {result && (
        <div style={{ marginTop: "2rem", backgroundColor: "#242424", padding: "1rem", borderRadius: "8px" }}>
          <h2>Analysis Result</h2>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            <li style={{ margin: "0.5rem 0" }}><strong>Name:</strong> {result.name}</li>
            <li style={{ margin: "0.5rem 0" }}><strong>Email:</strong> {result.email || "Not found"}</li>
            <li style={{ margin: "0.5rem 0" }}><strong>Phone:</strong> {result.phone}</li>
            <li style={{ margin: "0.5rem 0" }}><strong>Skills:</strong> {result.skills.join(", ")}</li>
            <li style={{ margin: "0.5rem 0" }}><strong>Predicted Roles:</strong> {result.predicted_roles.join(", ")}</li>
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