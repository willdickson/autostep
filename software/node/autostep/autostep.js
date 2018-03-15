"use strict";

let SerialDevice = require('./serialdevice');

const BAUDRATE = 115200;

class Autostep {

  constructor(port, callback) {
    this.hardwareVariant = null;
    this.device = new SerialDevice(port, {buadRate: BAUDRATE}, callback);
  }


  enable(callback) {
    let cmd = {command: 'enable'};
    this._sendCmdGetRsp(cmd, (err, rsp) =>  {
      if (callback) callback(err, rsp); 
    });
  }


  release(callback) {
    let cmd = {command: 'release'};
    this._sendCmdGetRsp(cmd, (err, rsp) =>  {
      if (callback) callback(err, rsp); 
    });
  }

  run(velocity, callback) {
    let cmd = {command: 'run', velocity: velocity};
    this._sendCmdGetRsp(cmd, (err, rsp) =>  {
      if (callback) callback(err, rsp); 
    });
  }


  // --------------------------------------------------------------------------- 
  _getCmdRsp(err, msg) {
    if (err) {
      return {success: false};
    } else {
      let msgObj = JSON.parse(msg);
      return msgObj;
    }
  }


  _sendCmd(cmd, callback) {
    this.device.sendCmd(JSON.stringify(cmd), callback);
  };


  _sendCmdGetRsp(cmd, callback) {
    var wrappedCallback = (err,msg) => {
      let rsp = this._getCmdRsp(err, msg);
      callback(err,rsp);
    };

    this._sendCmd(cmd, wrappedCallback);
  };


}

module.exports = Autostep;
