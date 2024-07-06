const express = require('express');
const axios = require('axios');
require('dotenv').config();  // Load environment variables from .env file

const app = express();
const port = process.env.PORT || 3000;

app.get('/api/hello', async (req, res) => {
  const visitorName = req.query.visitor_name;
  const clientIp = req.headers['x-forwarded-for'] || req.connection.remoteAddress;

  try {
    // Get location based on IP
    const locationResponse = await axios.get(`http://ip-api.com/json/${clientIp}`);
    const locationData = locationResponse.data;
    const city = locationData.city;

    // Get weather information
    const apiKey = process.env.OPENWEATHERMAP_API_KEY;
    const weatherResponse = await axios.get(`http://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`);
    const weatherData = weatherResponse.data;
    const temperature = weatherData.main.temp;

    res.json({
      client_ip: clientIp,
      location: city,
      greeting: `Hello, ${visitorName}!, the temperature is ${temperature} degrees Celsius in ${city}`
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

module.exports = app;
