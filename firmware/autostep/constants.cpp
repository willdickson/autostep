#include "constants.h"
#include <Arduino.h>

const long Baudrate = 115200;

const int Angle_Sensor_Pin = A1;
const int Stepper_Driver_Board_Num = 0;
const int Stepper_Driver_CS_Pin = 10;
const int Stepper_Driver_Reset_Pin = 7;
const int Stepper_Driver_Busy_Pin = 8;
const int RC_Servo_Pin = 3;
const int RC_PWM_Width_Min = 900;
const int RC_PWM_Width_Max = 1980;
const int RC_Servo_Alt_Pin = 14;
const int RC_PWM_Width_Min_Alt = 900;
const int RC_PWM_Width_Max_Alt = 1980;
const int Home_Pin = 2;
const int Default_Home_Polarity = LOW;

const uint32_t Timer_Period = 1000;
const float Position_Gain = 50.0;
const float Velocity_FFwd = 1.0;
const int Autoset_Num_Sample = 50;
