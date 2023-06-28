// Retrieve CSRF token from a cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Get the current ad ID from the URL
const getCurrentAdId = () => {
  const url = window.location.href;
  const adId = url.split('/').pop();
  return adId;
};

// Update the URL to navigate to the previous ad
const navigateToPreviousAd = () => {
  const currentAdId = getCurrentAdId();
  const previousAdId = parseInt(currentAdId) - 1;
  const previousAdUrl = `http://localhost:8000/crawler/${previousAdId}`;

  // Check if the page exists, if not, keep decrementing the ad ID
  checkAdUrlExists(previousAdUrl, navigateToPreviousAd, navigateToNextAd);
};

// Update the URL to navigate to the next ad
const navigateToNextAd = () => {
  const currentAdId = getCurrentAdId();
  const nextAdId = parseInt(currentAdId) + 1;
  const nextAdUrl = `http://localhost:8000/crawler/${nextAdId}`;

  // Check if the page exists, if not, keep incrementing the ad ID
  checkAdUrlExists(nextAdUrl, navigateToNextAd, navigateToPreviousAd);
};

// Check if the ad URL exists, if not, keep retrying with updated ad IDs
const checkAdUrlExists = (adUrl, onSuccess, onFail) => {
  fetch(adUrl)
    .then(response => {
      if (response.ok) {
        window.location.href = adUrl;
      } else {
        onFail();
      }
    })
    .catch(() => {
      onFail();
    });
};

// Add event listeners to the previous and next ad buttons
const previousAdButton = document.getElementById('previousAdButton');
previousAdButton.addEventListener('click', navigateToPreviousAd);

const nextAdButton = document.getElementById('nextAdButton');
nextAdButton.addEventListener('click', navigateToNextAd);



// function to upadte form data 
  const adId = getCurrentAdId();

   // Function to handle form submission
   function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

    const noteInput = document.getElementById('noteInput').value;
    const url = `http://localhost:8000/v1/crawler/update_ad/${adId}`;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();
    xhr.open('PUT', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    // Set up a callback function to handle the request response
    xhr.onload = function () {
      if (xhr.status === 200) {
        // Request successful, display the note or update the page as needed
        console.log('Note saved successfully');
      } else {
        // Request failed, handle the error appropriately
        console.error('Failed to save note:', xhr.status);
      }
    };

    // Create a JSON payload with the note data
    const payload = JSON.stringify({ notes: noteInput });

    // Send the PUT request
    xhr.send(payload);
  }

  // Attach the form submission handler
  const form = document.getElementById('notesForm');
  form.addEventListener('submit', handleSubmit);
