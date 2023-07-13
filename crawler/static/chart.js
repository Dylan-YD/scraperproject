function createBarChart(data) {
    // Extract the queries from the response data
    const queries = data.data.map(item => item.query);

    // Count the occurrences of each query
    const queryCount = {};
    queries.forEach(query => {
      queryCount[query] = (queryCount[query] || 0) + 1;
    });

    // Prepare data for the chart
    const queryLabels = Object.keys(queryCount);
    const queryValues = Object.values(queryCount);

    // Create the bar chart
    const ctx = document.getElementById('barChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: queryLabels,
        datasets: [{
          label: 'Query Count',
          data: queryValues,
          backgroundColor: 'rgba(0, 123, 255, 0.6)',
          borderColor: 'rgba(0, 123, 255, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            stepSize: 1
          }
        }
      }
    });
  }

  // Make the GET request to the specified route
  fetch("http://54.205.89.138:8001/v1/scraper") // Update the URL with the appropriate protocol (http/https)
    .then(response => response.json())
    .then(data => {
      createBarChart(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });



// Fetch data from URL
fetch('http://54.205.89.138:8001/v1/scraper')
.then(response => response.json())
.then(data => {
  // Check if the data has the expected structure
  if (data && data.data && Array.isArray(data.data) && data.data.length > 0) {
    // Extract the disposition data from the response
    const dispositionData = data.data.map(item => item.disposition);

    // Remove empty dispositions and count occurrences
    const dispositionCounts = dispositionData.filter(disposition => disposition !== "")
      .reduce((counts, disposition) => {
        counts[disposition] = (counts[disposition] || 0) + 1;
        return counts;
      }, {});

    // Handle null values and label them as "No Action"
    const nullCount = data.data.filter(item => item.disposition === "").length;
    if (nullCount > 0) {
      dispositionCounts["No Action"] = nullCount;
    }

    // Prepare labels and values for the chart
    const labels = Object.keys(dispositionCounts);
    const values = Object.values(dispositionCounts);

    // Render pie chart using Chart.js
    const ctx = document.getElementById('pieChart').getContext('2d');
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            // Add more colors if needed
          ],
        }],
      },
    });
  } else {
    console.error('Invalid data:', data);
  }
})
.catch(error => {
  console.error('Error:', error);
});