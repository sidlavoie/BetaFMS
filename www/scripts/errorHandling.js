// Function to handle the response from the server
function handleErrorResponse(response) {
  if (response.ok) {
      // Handle successful response here
  } else {
    response.json().then(data => {
      // Check if the error property exists in the JSON
      if (data && data.error) {
        // Generate HTML content for the error message and return button
        var errorPageHTML = '<div id="errorPage" style="text-align: center; padding: 20px;">';
        errorPageHTML += '<h2 style="color: #cc0000;">Error</h2>';
        errorPageHTML += '<p>' + data.error + '</p>';
        errorPageHTML += '<button onclick="redirectToHome()">Return</button>';
        errorPageHTML += '</div>';

        // Replace the entire body content with the error page HTML
        document.body.innerHTML = errorPageHTML;
      }
    });
  }
}

// Function to redirect to the home page
function redirectToHome() {
  window.location.href = '/';
}
