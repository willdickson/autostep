"use strict";

let Autostep = require('./autostep');


let stepper = new Autostep('/dev/ttyACM0', async (err) => {

  if (err) {
    console.log('open failed: ' + err);
  } else {

    let rsp = await stepper.enable();
    console.log(rsp);



    stepper.run(100, (err,rsp) => {
      if (err) {
        console.log(err)
      } else {
        console.log(rsp);
      }
    });


  }
}); 






