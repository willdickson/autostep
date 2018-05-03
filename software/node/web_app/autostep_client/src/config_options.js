"use strict";

const fullstepsPerRevOption = {
  label: 'Fullsteps Per Revolution',
  type: 'select',
  options: [ 
    {value: 200, text: '200'},
    {value: 400, text: '400'}
  ]
}; 

const stepModeOption = {
  label: 'Step Mode',
  type: 'select',
  options: [
    {value: 'STEP_FS',     option: 'STEP_FS'},
    {value: 'STEP_FS_2',   option: 'STEP_FS_2'},
    {value: 'STEP_FS_4',   option: 'STEP_FS_4'},
    {value: 'STEP_FS_8',   option: 'STEP_FS_8'},
    {value: 'STEP_FS_16',  option: 'STEP_FS_16'},
    {value: 'STEP_FS_32',  option: 'STEP_FS_32'},
    {value: 'STEP_FS_64',  option: 'STEP_FS_64'},
    {value: 'STEP_FS_128', option: 'STEP_FS_128'}
  ]
};

const overcurrentThreshold = {
  label: 'Over Current Threshold',
  type: 'select',
  options: [
    {value: 'OC_375mA',   option: 'OC_375mA'},  
    {value: 'OC_750mA',   option: 'OC_750mA'},
    {value: 'OC_1125mA',  option: 'OC_1125mA'},
    {value: 'OC_1500mA',  option: 'OC_1500mA'},
    {value: 'OC_1875mA',  option: 'OC_1875mA'},
    {value: 'OC_2250mA',  option: 'OC_2250mA'},
    {value: 'OC_2625mA',  option: 'OC_2625mA'},
    {value: 'OC_3000mA',  option: 'OC_3000mA'},
    {value: 'OC_3375mA',  option: 'OC_3375mA'},
    {value: 'OC_3750mA',  option: 'OC_3750mA'},
    {value: 'OC_4125mA',  option: 'OC_4125mA'},
    {value: 'OC_4500mA',  option: 'OC_4500mA'},
    {value: 'OC_4875mA',  option: 'OC_4875mA'},
    {value: 'OC_5250mA',  option: 'OC_5250mA'},
    {value: 'OC_5625mA',  option: 'OC_5625mA'},
    {value: 'OC_6000mA',  option: 'OC_6000mA'}
  ]
};

export const configOptions = [
  fullstepsPerRevOption,
  stepModeOption,
  overcurrentThreshold,
];


