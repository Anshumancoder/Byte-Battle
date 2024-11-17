const form = document.getElementById('locationForm');
const pollutionInfo = document.getElementById('pollution-info');
const solutions = document.getElementById('solutions');
const resultsSection = document.getElementById('results');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const location = document.getElementById('location').value;
  if (!location) {
    alert('Please enter a location!');
    return;
  }

  try {
    // Get coordinates for the location
    const geoResponse = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${location}`);
    const geoData = await geoResponse.json();

    if (geoData.length === 0) {
      alert('Location not found. Please try again.');
      return;
    }

    const { lat, lon, display_name } = geoData[0];

    // Get pollution data for the location
    const pollutionResponse = await fetch(
      `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&hourly=pm10,pm2_5`
    );
    const pollutionData = await pollutionResponse.json();

    // Log the API response for debugging
    console.log('Pollution API Response:', pollutionData);

    // Check if hourly pollution data exists
    if (!pollutionData.hourly || !pollutionData.hourly.pm10 || pollutionData.hourly.pm10.length === 0 || !pollutionData.hourly.pm2_5 || pollutionData.hourly.pm2_5.length === 0) {
      alert('No pollution data available for this location. This might be due to data unavailability in the API.');
      console.error('Pollution data structure issue or missing data:', pollutionData);
      pollutionInfo.innerHTML = `<p><strong>Location:</strong> ${display_name}</p>
                                 <p>Unfortunately, no pollution data is available for this location.</p>`;
      resultsSection.classList.remove('hidden');
      return;
    }

    // Display the first hourly pollution data (assuming today’s first reading)
    const pm10Now = pollutionData.hourly.pm10[0];
    const pm25Now = pollutionData.hourly.pm2_5[0];
    pollutionInfo.innerHTML = `
      <p><strong>Location:</strong> ${display_name}</p>
      <p><strong>PM10 Concentration (Now):</strong> ${pm10Now} µg/m³</p>
      <p><strong>PM2.5 Concentration (Now):</strong> ${pm25Now} µg/m³</p>
    `;

    // Suggestions based on PM2.5 levels
    solutions.innerText = getSuggestions(pm25Now);

    // Display results section
    resultsSection.classList.remove('hidden');

    // Render pollution graph using hourly data
    renderPollutionGraph(pollutionData.hourly);
  } catch (error) {
    alert('Error fetching data. Please try again later.');
    console.error('Error:', error);
  }
});

// Function to get pollution suggestions
function getSuggestions(pm25) {
  if (pm25 <= 12) return 'The pollution in your area is good. Keep up the good work!';
  if (pm25 <= 35) return 'Air quality is moderate. Try adopting more eco-friendly practices.';
  if (pm25 <= 55) return 'Air quality is unhealthy for sensitive groups. Reduce pollution wherever possible.';
  if (pm25 <= 150) return 'Air quality is unhealthy. Wear a mask outdoors and try to minimize outdoor activities.';
  return 'Air quality is very unhealthy. Stay indoors and consider using air purifiers.';
}

// Function to render pollution graph using Chart.js
function renderPollutionGraph(hourlyData) {
  const ctx = document.getElementById('pollutionChart').getContext('2d');

  // Extract time labels and PM10/PM2.5 values
  const labels = hourlyData.time; // Assuming time is an array of timestamps
  const pm10Values = hourlyData.pm10; // PM10 data
  const pm25Values = hourlyData.pm2_5; // PM2.5 data

  if (labels.length === 0 || pm10Values.length === 0 || pm25Values.length === 0) {
    console.error('No data available for chart rendering');
    return;
  }

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'PM10 Concentration (µg/m³)',
          data: pm10Values,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderWidth: 1,
        },
        {
          label: 'PM2.5 Concentration (µg/m³)',
          data: pm25Values,
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Pollution Levels Over Time',
        },
      },
    },
  });
}
