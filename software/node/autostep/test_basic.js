"use strict";

let Autostep = require('./autostep');

const runStepper = async function()  {

  const stepper = await Autostep.createNew('/dev/ttyACM0');

  await stepper.printParams();

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








