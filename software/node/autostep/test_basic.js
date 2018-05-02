"use strict";

let Autostep = require('./autostep');


const runStepper = async function()  {

  const stepper = await Autostep.createNew('/dev/ttyACM0');

  let rsp = null;

  rsp = await stepper.setMoveModeToMax();
  console.log(rsp);

  rsp = await stepper.enable(); 
  console.log(rsp);

  await stepper.printParams();

  const params = { 
    amplitude: 180.0,
    period:  5.0,
    phase:  90.0,
    offset: 0.0, 
    num_cycle: 2 
  }

  const print_data = (err, data) => {
    if (data) {
      console.log(data);
    } 
  };

  rsp = await stepper.sinusoid(params,null,print_data);
  console.log(rsp);

  //let rsp = null;
  //let step = 360;
  //let num = 5;

  //for (let pos=0; pos<num*step; pos+=step) {

  //  console.log('pos = ' + pos);

  //  rsp = await stepper.moveTo(pos);
  //  await stepper.busyWait();

  //  rsp = await stepper.getPosition();
  //  console.log(rsp);
  //  console.log();

  //}

  //rsp = await stepper.moveTo(0);
  //await stepper.busyWait();

  //rsp = await stepper.getPosition();
  //console.log(rsp);
  //console.log();


}
runStepper();








