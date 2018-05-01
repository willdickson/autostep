"use strict";
const util = require('util');
const path = require('path');
const express = require('express');
const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);
const Autostep = require('autostep');
const _ = require('lodash');

// Run parameters
const serialPortName = '/dev/ttyACM0';
const networkPort = 5000;

const clientDistDir = path.join(__dirname, '../autostep_client/dist');
const staticFileDir = path.join(clientDistDir, 'static');


// Setup Autostep stepper
// --------------------------------------------------------------------------------------

const stepper = new Autostep(serialPortName, async () => {
  console.log('* stepper connected');

  let rsp = null;

  rsp = await stepper.setMoveModeToJog();
  if (rsp.success) {
    console.log('* move mode set to jog');
  } else {
    console.log('* failed to set move mode');
  }

  rsp = await stepper.enable();
  if (rsp.success) {
    console.log('* stepper enabled');
  } else {
    console.log('* failed to enable stepper');
  }

  rsp = await stepper.moveTo(0);
  if (rsp.success) {
    console.log('* stepper zeroed');
  } else {
    console.log('* failed to zero stepper');
  }

  await stepper.printParams();
});


// Setup Server
// --------------------------------------------------------------------------------------

app.use('/static', express.static(staticFileDir))
server.listen(networkPort);


app.get('/', function (req, res) {
    res.sendFile(path.join(clientDistDir, 'index.html'));
});

io.on('connection', function (socket) {

  console.log('* got new connection');

  socket.on('testMessage', async function (data) {
    console.log('got testMessage: ' + JSON.stringify(data));
  });

});

console.log();
console.log('* listening on port: ' + networkPort);


// SIGINT exit handler
// --------------------------------------------------------------------------------------
process.on('SIGINT', (code) => {
  console.log();
  console.log();
  console.log('* quiting');
  console.log();
  process.exit(0);
});



