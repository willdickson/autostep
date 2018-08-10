"use strict";

let Autostep = require('./autostep');


const runStepper = async function()  {

  const stepper = await Autostep.createNew('/dev/ttyACM0');
  stepper.setGearRatio(2.0);

  //let params = await stepper.getParams();
  //console.log(params);
  //console.log(params);
  //let rsp = await stepper.setParams(params);
  //params = await stepper.getParams();
  //console.log(params);

  await stepper.printParams();

  if (true) {
    let rsp = null;

    rsp = await stepper.setMoveModeToJog();
    console.log(rsp);

    rsp = await stepper.enable(); 
    console.log(rsp);

    await stepper.printParams();

    rsp = await stepper.moveTo(0);
    console.log(rsp)
    await stepper.busyWait();
    await stepper.sleep(1.0);

    const params = { 
      amplitude: 180.0,
      period:  5.0,
      phase:  90.0,
      offset: 0.0, 
      num_cycle: 1 
    }

    rsp = await stepper.moveToSinusoidStart(params);
    console.log(rsp);
    await stepper.busyWait();
    await stepper.sleep(1.0);

    rsp = await stepper.sinusoid(params,null,(err,data)=> {});
    console.log(rsp);
    await stepper.busyWait()
    await stepper.sleep(1.0);

    rsp = await stepper.setMoveModeToJog();
    rsp = await stepper.moveTo(0);
    console.log(rsp)
    await stepper.busyWait();


  }

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








