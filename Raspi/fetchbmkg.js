const axios = require('axios');
const xml2js = require('xml2js');
const fs = require('fs');
const outputJsonFile = 'output.json';

// Define the API URL
const apiUrl = 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml'; // Replace with your API URL

// Make an HTTP GET request to the API
function fetchData(){
  axios.get(apiUrl)
  .then((response) => {
    // Check if the response status is 200 (OK)
    if (response.status === 200) {
      // Parse the XML data using xml2js
      xml2js.parseString(response.data, (err, result) => {
        if (err) {
          console.error('Error parsing XML:', err);
        } else {
          console.log(result.data.forecast[0].area[26]);
          // The parsed XML data is in the 'result' object
          const jsonData = JSON.stringify(result.data.forecast[0].area[26].parameter[6]);
          fs.writeFileSync(outputJsonFile, jsonData, 'utf8');
          console.log('Data saved to', outputJsonFile);
        }
      });
    } else {
      console.error('Error fetching data from the API. Status:', response.status);
    }
  })
  .catch((error) => {
    console.error('Error fetching data from the API:', error);
  });
}

fetchData();

// Set an interval to fetch data every 6 hours (2.16e+7 milliseconds)
const interval = 2.16 * 10000000; // 
setInterval(fetchData, interval);

