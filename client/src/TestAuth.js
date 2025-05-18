import axios from 'axios';

// Simple test function to debug registration
async function testRegistration() {
  try {
    console.log("Testing registration with test user...");
    
    const userData = {
      username: "testuser2",
      password: "testpassword2",
      email: "test2@example.com",
      full_name: "Test User 2"
    };
    
    console.log("Sending data:", userData);
    
    const response = await axios.post("http://localhost:8000/register", userData);
    console.log("Registration successful:", response.data);
    
    return "Registration successful!";
  } catch (error) {
    console.error("Registration error:", error);
    
    if (error.response) {
      console.error("Response data:", error.response.data);
      console.error("Response status:", error.response.status);
      console.error("Response headers:", error.response.headers);
      return `Registration failed with status ${error.response.status}: ${JSON.stringify(error.response.data)}`;
    }
    
    return `Registration failed: ${error.message}`;
  }
}

// Test the validation debug endpoint
async function testValidation() {
  try {
    const response = await axios.post("http://localhost:8000/debug/register");
    console.log("Validation test result:", response.data);
    return "Validation test complete. Check console for details.";
  } catch (error) {
    console.error("Validation test error:", error);
    return `Validation test failed: ${error.message}`;
  }
}

// Function to check registered users
async function checkUsers() {
  try {
    const response = await axios.get("http://localhost:8000/debug/users");
    console.log("Registered users:", response.data);
    return `Found ${response.data.count} registered users: ${response.data.users.join(", ")}`;
  } catch (error) {
    console.error("Error checking users:", error);
    return `Failed to check users: ${error.message}`;
  }
}

// Test login with the pre-seeded test user
async function testLogin() {
  try {
    const params = new URLSearchParams();
    params.append("username", "testuser");
    params.append("password", "testpassword");
    
    const response = await axios.post("http://localhost:8000/token", params);
    console.log("Login successful:", response.data);
    return "Login successful! Token received.";
  } catch (error) {
    console.error("Login error:", error);
    
    if (error.response) {
      return `Login failed with status ${error.response.status}: ${JSON.stringify(error.response.data)}`;
    }
    
    return `Login failed: ${error.message}`;
  }
}

// Export the test functions
export { testRegistration, testValidation, checkUsers, testLogin };