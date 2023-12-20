$(document).ready(function() {
    // Perform AJAX request to fetch the dynamic data
    $.ajax({
      url: `${baseURL}/v1/scraper/number_of_ads`,
      type: 'GET',
      success: function(response) {
        var numberOfAds = response.data;
        $('#number-of-ads').text(numberOfAds);
      },
      error: function() {
        $('#number-of-ads').text('Error retrieving data.');
      }
    });
  });


  $(document).ready(function() {
    // Perform AJAX request to fetch the dynamic data
    $.ajax({
      url: `${baseURL}/v1/scraper/ad_queries_count`,
      type: 'GET',
      success: function(response) {
        var numberOfAds = response.data;
        $('#ad-queries-count').text(numberOfAds);
      },
      error: function() {
        $('#ad-queries-count').text('Error retrieving data.');
      }
    });
  });




   // Function to fetch and populate data
   function fetchData() {
    // Make an AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `${baseURL}/v1/scraper`, true);

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.status === 200) {
          var data = response.data;
          populateTable(data); // Call function to populate table with the fetched data
        }
      }
    };

    xhr.send();
  }


  // Define the data variable in a higher scope
var data = [];
// Function to populate the table with data
function populateTable(data) {
  var tableBody = document.querySelector("#projectTable tbody");

  // Clear existing table rows
  tableBody.innerHTML = "";

  // Iterate over the data and create table rows
  data.forEach(function (project) {
    var row = document.createElement("tr");

    // Create table cells for each project property
    var adIdCell = document.createElement("td");
    adIdCell.textContent = project.ad_id;
    row.appendChild(adIdCell);

    var adTitleCell = document.createElement("td");
    var created_at = project.created_at;
    var created_date = created_at.split("T")[0];
    adTitleCell.innerHTML = `
      <a>${project.ad_title}</a>
      <br/>
      <small>Created ${created_date}</small>
    `;
    row.appendChild(adTitleCell);

    var adScreenshotCell = document.createElement("td");
    var adScreenshotLink = document.createElement("a");
    adScreenshotLink.href = project.screenshot;
    adScreenshotLink.target = "_blank";
    var adScreenshot = document.createElement("img");
    adScreenshot.className = "table-avatar";
    adScreenshot.src = project.screenshot;
    adScreenshotLink.appendChild(adScreenshot);
    adScreenshotCell.appendChild(adScreenshotLink);
    row.appendChild(adScreenshotCell);

    var queryCell = document.createElement("td");
    queryCell.textContent = project.query;
    row.appendChild(queryCell);

    var adDescriptionCell = document.createElement("td");
    adDescriptionCell.textContent = project.ad_description;
    row.appendChild(adDescriptionCell);

    var adUrlCell = document.createElement("td");
    var adUrlLink = document.createElement("a");
    adUrlLink.href = project.ad_url;
    adUrlLink.textContent = "View";
    adUrlCell.appendChild(adUrlLink);
    row.appendChild(adUrlCell);

    var actionsCell = document.createElement("td");
    actionsCell.className = "project-actions text-right";
    actionsCell.innerHTML = `
    <a class="btn btn-info btn-sm" href='${baseURL}/crawler/${project.ad_id}'>
    <i class="fas fa-pencil-alt"></i>
    Edit
  </a>
      <a class="btn btn-danger btn-sm delete-button" href="#" data-ad-id="${project.ad_id}">
        <i class="fas fa-trash"></i>
        Delete
      </a>
    `;
    row.appendChild(actionsCell);

    tableBody.appendChild(row);
  });

  // Add event listener for image click to display a popup with a larger image
  var adScreenshots = document.querySelectorAll(".table-avatar");
  adScreenshots.forEach(function (adScreenshot) {
    adScreenshot.addEventListener("click", function () {
      var imageUrl = adScreenshot.src;
      var popup = window.open("", "_blank", "width=500,height=200");
      popup.document.write(
        `<img src="${imageUrl}" style="width: 100%; height: 100%;" />`
      );
    });
  });

  // Add event listeners to the delete buttons
  var deleteButtons = document.querySelectorAll(".delete-button");
  deleteButtons.forEach(function (deleteButton) {
    deleteButton.addEventListener("click", function (event) {
      event.preventDefault();
      var row = deleteButton.closest("tr");
      var adId = deleteButton.getAttribute("data-ad-id");
      showDeleteConfirmation(adId, row);
    });
  });

  // Function to show the delete confirmation popup
  function showDeleteConfirmation(adId, row) {
    if (confirm("Are you sure you want to delete this record?")) {
      deleteAd(adId, row);
    }
  }

  // Function to delete an ad
  function deleteAd(adId, row) {
    // Send a DELETE request to the server
    var csrfToken = getCookie("csrftoken");
    fetch(`${baseURL}/v1/crawler/delete_ad/${adId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then(function (response) {
        if (response.ok) {
          // Delete the row from the UI
          row.parentNode.removeChild(row);
        } else {
          throw new Error("Failed to delete ad");
        }
      })
      .catch(function (error) {
        console.error(error);
      });
  }

  // Function to get the value of a cookie by name
  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) {
      return parts.pop().split(";").shift();
    }
  }
}



  
  // Function to filter the table based on the search query
  function filterTable() {
    var searchInput = document.querySelector("#searchInput");
    var filter = searchInput.value.toUpperCase();
    var tableRows = document.querySelectorAll("#projectTable tbody tr");
  
    tableRows.forEach(function (row) {
      var queryCell = row.querySelector("td:nth-child(4)");
      var queryText = queryCell.textContent.toUpperCase();
  
      if (queryText.indexOf(filter) > -1) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  }
  
  // Fetch and populate data
  fetchData();
  
  // Add event listener
  

