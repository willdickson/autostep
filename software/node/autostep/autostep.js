"use strict";
const util = require('util');

let SerialDevice = require('./serialdevice');

const BAUDRATE = 115200;

class Autostep {

  constructor(port, callback) {
    this.hardwareVariant = null;
    this.device = new SerialDevice(port, {buadRate: BAUDRATE}, callback);
  }

  enable(callback) { 
    const cmd = {command: 'enable'};
    return this._sendCmd(cmd,callback);
  }

  release(callback) {
    const cmd = {command: 'release'};
    return this._sendCmd(cmd,callback);
  }

  run(velocity, callback) {
    const cmd = {command: 'run', velocity: velocity};
    return this._sendCmd(cmd,callback);
  }

  _sendCmd(cmd, callback) {
    const promise = new Promise((resolve,reject) => {
      this.device.sendCmd(JSON.stringify(cmd), (err,rsp) => {
        if (err) {
          reject(err);
        } else {
          let rspObj = null;
          try {
            rspObj = JSON.parse(rsp);
          } catch(err) {
            reject(err);
          }
          resolve(rspObj);
        }
      });
    });

    if (callback && typeof callback == 'function') {
      promise
        .then(  (rsp) => callback(null,rsp))
        .catch( (err) => callback(err,null));
    }
    return promise;
  };
}

module.exports = Autostep;
