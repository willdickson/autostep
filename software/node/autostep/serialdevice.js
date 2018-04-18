"use strict";

const SerialPort = require('serialport');
const parser = new SerialPort.parsers.Readline({
  delimiter: '\n',
});


class SerialDevice {

  constructor(port, options, openCallback) {

    this.busy = false;
    this.cmdQueue = [];
    this.cmdCurrent = null;
    this.serial = new SerialPort(port,options);
    this.serial.pipe(parser);
    this.streamCallback = null;
  
    if (openCallback && typeof openCallback == 'function') {
      this.serial.on('open', openCallback);
    }
    let dataCallback = (data) => {
      if (!this.cmdCurrent) {
        if (this.streamCallback) {
          let dataObj = null;
          let parseErr = null;
          try {
            dataObj = JSON.parse(data);
          } catch (err) {
            parseErr = err;
          }
          this.streamCallback(parseErr, dataObj);
        }
        return;
      } 

      let moreFlag = false;
      if (this.cmdCurrent.callback) { 
        moreFlag = this.cmdCurrent.callback(null,data)
      }
      if (moreFlag) {
        this.cmdQueue.unshift({
          message: null, 
          callback: this.cmdCurrent.callback
        });
      } 
      this.processQueue();
    }
    this.serial.on('data', dataCallback); 
  }

  setStreamCallback(streamCallback)
  {
    this.streamCallback = streamCallback;
  }

  sendCmd(data,callback) {
    this.cmdQueue.push({message: data, callback: callback});
    if (this.busy) {
      return;
    }
    this.busy = true;
    this.processQueue();
  }

  processQueue() {
    let cmdNext  = this.cmdQueue.shift();
    if (!cmdNext) {
      this.busy = false;
      this.cmdCurrent = null; 
      return;
    }
    this.cmdCurrent = cmdNext;
    if (cmdNext.message) {
      this.serial.write(cmdNext.message + '\n', (err) =>  {
        if (err) {
          if (cmdNext.callback) cmdNext.callback(err,null);
        }
      });
    }
  }

}

module.exports = SerialDevice;

const BAUDRATE = 115200;

