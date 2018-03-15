"use strict";

let Autostep = require('./autostep');


let stepper = new Autostep('/dev/ttyACM0', (err) => {

  if (err) {
    console.log('open failed: ' + err);
  } else {

    stepper.enable((err,rsp) => {
      if (err) {
        console.log(err)
      } else {
        console.log(rsp);
      }
    });

    stepper.run(100, (err,rsp) => {
      if (err) {
        console.log(err)
      } else {
        console.log(rsp);
      }
    });


  }
}); 






