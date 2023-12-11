// Load the number of ads from the API

fetch("http://127.0.0.1:8000/v1/scraper/number_of_ads")
.then(response => response.json())
.then(data => {
  // Update the HTML with the retrieved data
  const adCountElement = document.getElementById("adCount");
  adCountElement.textContent = data.data;
})
.catch(error => {
  console.error("Error fetching ad count:", error);
});


// v1/scraper/ad_queries_count'
fetch("http://127.0.0.1:8000/v1/scraper/ad_queries_count")
.then(response => response.json())
.then(data => {
  // Update the HTML with the retrieved data
  const adCountElement = document.getElementById("queryCount");
  adCountElement.textContent = data.data;
})
.catch(error => {
  console.error("Error fetching ad count:", error);
});


// send a post request to the API when the query form is submitted
const form = document.getElementById("searchForm");
form.addEventListener("submit", event => {
    event.preventDefault();
    const formData = new FormData(form);
    const query = formData.get("query");
    const url = `http://127.0.0.1:8000/v1/scraper/${query}`;
    fetch(url, { method: "POST" })
    .then(response => response.json())
    .then(data => {
        // Update the HTML with the retrieved data
        const queryCountElement = document.getElementById("queryCount");
        queryCountElement.textContent = data.data;
    })
    .catch(error => {
        console.error("Error fetching query count:", error);
    });
    }
);

document.getElementById('searchForm').addEventListener('submit', function(e) {
  e.preventDefault(); // Prevent the form from submitting normally

  var form = e.target;
  var csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
  var query = form.querySelector('#queryInput').value;

  fetch('http://127.0.0.1:8000/v1/scraper/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ query: query })
  })
  .then(response => {
    // Handle the response
  })
  .catch(error => {
    // Handle errors
  });
});

//getting all the ads
  // Fetch data from local54.205.89.138host:8001/v1/scraper
  fetch('http://127.0.0.1:8000/v1/scraper')
    .then(response => response.json())
    .then(data => {
      if (data.status === 200) {
        const tableBody = document.getElementById('data-placeholder');
        let tableHTML = '';

        data.data.forEach(item => {
          tableHTML += `
            <tr>
              <td>
                <label class="users-table__checkbox">
                  <input type="checkbox" class="check">
                  <div class="categories-table-img">
                    <picture>
                      <source srcset="${item.screenshot}" type="image/webp">
                      <img src="./img/categories/01.jpg" alt="category">
                    </picture>
                  </div>
                </label>
              </td>
              <td>${item.ad_title}</td>
              <td>${item.ad_description}</td>
              <td><span class="badge-pending">On action</span></td>
              <td>10/02/2022</td>
              <td>
                <span class="p-relative">
                  <button class="dropdown-btn transparent-btn" type="button" title="More info">
                    <div class="sr-only">More info</div>
                    <i data-feather="more-horizontal" aria-hidden="true"></i>
                  </button>
                  <ul class="users-item-dropdown dropdown">
                    <li><a href="##">Edit</a></li>
                    <li><a href="##">Quick edit</a></li>
                    <li><a href="##">Trash</a></li>
                  </ul>
                </span>
              </td>
            </tr>
          `;
        });

        tableBody.innerHTML = tableHTML;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });