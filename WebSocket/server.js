const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors'); // Import the cors module
const mqtt = require('mqtt');

const MQTT_BROKER_URL = 'mqtt://broker.mqtt-dashboard.com';
const MQTT_TOPIC = 'hafidzganteng/statusServoWeb';
const MQTT_TOPIC2 = 'hafidzganteng/statusLEDWeb';

const client = mqtt.connect(MQTT_BROKER_URL);

client.on('connect', () => {
  client.subscribe(MQTT_TOPIC, (err) => {
    if (!err) {
      console.log(`Connected to MQTT broker and subscribed to topic: ${MQTT_TOPIC}`);
    }
  });
  client.subscribe(MQTT_TOPIC2, (err) => {
    if (!err) {
      console.log(`Connected to MQTT broker and subscribed to topic: ${MQTT_TOPIC2}`);
    }
  });
});

const app = express();
app.use(cors({ origin: '*' }));

const server = http.createServer(app);
const io = socketIo(server, {
    cors:{
        origin: '*'
    }
});

// Use the cors middleware with appropriate configuration

io.on('connection', (socket) => {
  console.log('A client has connected to the WebSocket.');

  socket.on('disconnect', () => {
    console.log('A client has disconnected from the WebSocket.');
  });

  client.on('message', (topic, message) => {
    if(topic == MQTT_TOPIC){
      const payload = message.toString();
      var flag = parseInt(payload, 10);
      const intervalId = setInterval(() => {
        if(flag >= 0){
          io.emit('mqttMessage', flag);
          flag--;
        }
      }, 1000);
      if(flag == 0){
        clearInterval(intervalId);
      }
    }
    else if(topic == MQTT_TOPIC2 && message.toString() == "yes"){
      var flag = 10;
      const intervalId = setInterval(() => {
        if(flag >= 0){
          io.emit('mqttMessage2', flag);
          flag--;
        }
      }, 1000);
      if(flag == 0){
        clearInterval(intervalId);
      }
    }
  });
});

server.listen(3001, () => {
  console.log('Server is running on port 3001.');
});
