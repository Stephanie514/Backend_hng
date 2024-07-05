const express = require('express');
const requestIp = require('request-ip');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.get('/api/hello', (req, res) => {
  const visitorName = req.query.visitor_name || 'Guest';
  const clientIp = requestIp.getClientIp(req); // Retrieve client IP
  const location = 'New York'; // Static location for now

  const response = {
    client_ip: clientIp,
    location: location,
    greeting: `Hello, ${visitorName}!, the temperature is 11 degrees Celcius in ${location}`
  };

  res.json(response);
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
