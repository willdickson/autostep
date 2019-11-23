#ifndef CONSTANTS_H
#define CONSTANTS_H
#include <Arduino.h>

const int Serial_Buffer_Size = 1000;
const int Json_Message_Buffer_Size = 4000;
const int Json_Data_Buffer_Size = 500;

extern const long Baudrate;
extern const int Angle_Sensor_Pin;
extern const int Stepper_Driver_Board_Num;
extern const int Stepper_Driver_CS_Pin;
extern const int Stepper_Driver_Reset_Pin;
extern const int Stepper_Driver_Busy_Pin;
extern const int RC_Servo_Pin;

extern const uint32_t Timer_Period;
extern const float Position_Gain;
extern const float Velocity_FFwd;
extern const int Autoset_Num_Sample;

#endif
