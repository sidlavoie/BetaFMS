// Function to handle the response from the server
function handleErrorResponse(response) {
  if (response.ok) {
      // Handle successful response here
  } else {
    response.json().then(data => {
      openPopup('Error: ' + data.error);
    });
  }
}
  
  // Function to open the custom popup
function openPopup(message) {
    var popup = document.getElementById("customPopup");
    var popupMessage = document.getElementById("popupMessage");
    popupMessage.innerHTML = message;
    popup.style.display = "block";
}

  // Function to close the custom popup
function closePopup() {
    // Your code to close the popup
}

