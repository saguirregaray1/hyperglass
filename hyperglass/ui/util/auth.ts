async function authenticate() {

  try {
    const response = await fetch("http://localhost:8000/auth/token/", {
      method: 'POST',
      credentials: 'include', // Ensures the cookie is stored
      headers: {
        'Content-Type': 'application/json'
      },
      // Replace with your actual login credentials
      body: JSON.stringify({ email: 'admin@example.com', password: 'admin' })
    });
    if (!response.ok) {
      throw new Error(`Login error! Status: ${response.status}`);
    }
    // The cookie is automatically set by the browser.
    // Now add those cookie credentials to every subsequent request:
    applyCookieCredentialsToRequests();
  } catch (error) {
    console.error('Authentication failed:', error);
    responseOutput.textContent = 'Authentication failed: ' + error.message;
  }
}

/**
 * Overrides the global fetch function so that every request
 * automatically includes cookie credentials.
 */
function applyCookieCredentialsToRequests() {
  const originalFetch = window.fetch;
  window.fetch = (...args) => {
    // Ensure the options object exists and credentials is included
    const options = args[1] || {};
    return originalFetch(args[0], { ...options, credentials: 'include' });
  };
}
