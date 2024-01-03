// Function to handle the response from the server
function handleErrorResponse(response) {
    if (response.ok) {
        // Handle successful response here
    } else {
        response.json().then(data => {
            // Check if the error property exists in the JSON
            if (data && data.error) {
                // Load the error page dynamically
                loadErrorPage(data.error);
            }
        });
    }
}

// Function to load the error page dynamically
function loadErrorPage(errorMessage) {
    var errorContainer = document.createElement('div');
    errorContainer.id = 'errorContainer';
    errorContainer.style.textAlign = 'center';
    errorContainer.style.padding = '20px';

    var errorHeader = document.createElement('h2');
    errorHeader.style.color = '#cc0000';
    errorHeader.textContent = 'Error';

    var errorParagraph = document.createElement('p');
    errorParagraph.textContent = errorMessage;

    var returnButton = document.createElement('button');
    returnButton.textContent = 'Return';
    returnButton.onclick = redirectToHome;

    errorContainer.appendChild(errorHeader);
    errorContainer.appendChild(errorParagraph);
    errorContainer.appendChild(returnButton);

    // Replace the entire body content with the error container
    document.body.innerHTML = '';
    document.body.appendChild(errorContainer);
}

// Function to redirect to the home page
function redirectToHome() {
    window.location.href = '/';
}