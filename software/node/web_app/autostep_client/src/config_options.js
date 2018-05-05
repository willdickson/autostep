"use strict";
let _ = require('lodash');

const fullstepsPerRevOption = {
  label: 'Fullsteps/Revolution',
  type: 'select',
  options: [ 
    {value: 200, text: '200'},
    {value: 400, text: '400'}
  ],
  defaultValue: 200,
}; 

const stepModeOption = {
  label: 'Mircostep Mode',
  type: 'select',
  options: [
    {value: 'STEP_FS',     text: 'STEP_FS'},
    {value: 'STEP_FS_2',   text: 'STEP_FS_2'},
    {value: 'STEP_FS_4',   text: 'STEP_FS_4'},
    {value: 'STEP_FS_8',   text: 'STEP_FS_8'},
    {value: 'STEP_FS_16',  text: 'STEP_FS_16'},
    {value: 'STEP_FS_32',  text: 'STEP_FS_32'},
    {value: 'STEP_FS_64',  text: 'STEP_FS_64'},
    {value: 'STEP_FS_128', text: 'STEP_FS_128'}
  ],
  defaultValue: 'STEP_FS_64', 
};

const overcurrentThreshold = {
  label: 'Overcurrent Threshold',
  type: 'select',
  options: [
    {value: 'OC_375mA',   text: 'OC_375mA'},  
    {value: 'OC_750mA',   text: 'OC_750mA'},
    {value: 'OC_1125mA',  text: 'OC_1125mA'},
    {value: 'OC_1500mA',  text: 'OC_1500mA'},
    {value: 'OC_1875mA',  text: 'OC_1875mA'},
    {value: 'OC_2250mA',  text: 'OC_2250mA'},
    {value: 'OC_2625mA',  text: 'OC_2625mA'},
    {value: 'OC_3000mA',  text: 'OC_3000mA'},
    {value: 'OC_3375mA',  text: 'OC_3375mA'},
    {value: 'OC_3750mA',  text: 'OC_3750mA'},
    {value: 'OC_4125mA',  text: 'OC_4125mA'},
    {value: 'OC_4500mA',  text: 'OC_4500mA'},
    {value: 'OC_4875mA',  text: 'OC_4875mA'},
    {value: 'OC_5250mA',  text: 'OC_5250mA'},
    {value: 'OC_5625mA',  text: 'OC_5625mA'},
    {value: 'OC_6000mA',  text: 'OC_6000mA'}
  ],
  defaultValue: 'OC_3375mA',
};

const jogModeSpeed = {
  label: 'Jog Mode Speed (&deg/s)',
  type: 'number',
  minValue: 1,
  maxValue: 1000,
  defaultValue: 100,
};

const jogModeAccel = {
  label: 'Jog Mode Accel (&deg/s<sup>2</sup>)',
  type: 'number',
  minValue: 1,
  maxValue: 10000,
  defaultValue: 200,

};

const jogModeDecel = {
  label: 'Jog Mode Decel (&deg/s<sup>2</sup>)',
  type: 'number',
  minValue: 1,
  maxValue: 10000,
  defaultValue: 200,
};

const maxModeSpeed = {
  label: 'Max Mode Speed (&deg/s)',
  type: 'number',
  minValue: 1,
  maxValue: 2000,
  defaultValue: 1000,
};

const maxModeAccel = {
  label: 'Max Mode Accel (&deg/s<sup>2</sup>)',
  type: 'number',
  minValue: 1,
  maxValue: 20000,
  defaultValue: 8000,
};

const maxModeDecel = {
  label: 'Max Mode Decel (&deg/s<sup>2</sup>)',
  type: 'number',
  minValue: 1,
  maxValue: 20000,
  defaultValue: 8000,
};

const kvalOptionValues = _.range(1,256);
const kvalOptionTexts  = _.map(kvalOptionValues,String);
const kvalOptions = _.zipObject(kvalOptionValues ,kvalOptionTexts);

const kvalRun = {
  label: 'Kval Run',
  type: 'select',
  options: kvalOptions
};

const kvalHold = {
  label: 'Kval Hold',
  type: 'select',
  options: kvalOptions
};

const kvalAccel = {
  label: 'Kval Accel',
  type: 'select',
  options: kvalOptions
};

const kvalDecel = {
  label: 'Kval Decel',
  type: 'select',
  options: kvalOptions
};

export const configOptions = [
  fullstepsPerRevOption,
  stepModeOption,
  overcurrentThreshold,
  jogModeSpeed,
  jogModeAccel,
  jogModeDecel,
  maxModeSpeed,
  maxModeAccel,
  maxModeDecel,
  kvalAccel,
  kvalDecel,
  kvalRun,
  kvalHold,
];



