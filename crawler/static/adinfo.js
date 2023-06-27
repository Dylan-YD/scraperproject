// Retrieve CSRF token from a cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  // AJAX request to update the ad with the note
  const form = document.getElementById('notesForm');
  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    const notes = document.getElementById('noteInput').value.trim();
    // get adID from the URL
    const adId = window.location.href.split('/').pop();

    const url = `http://localhost:8000/v1/crawler/update_ad/${adId}`;
    console.log('URL:', url);
    const data = { notes: notes };
    const csrfToken = getCookie('csrf_token'); // Modify to match your CSRF token name
    console.log('CSRF Token:', csrfToken);

    fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
      .then(result => {
        console.log('Note saved:', result);
        // Handle success response as needed
      })
      .catch(error => {
        console.error('Error:', error);
        // Handle error as needed
      });
  });