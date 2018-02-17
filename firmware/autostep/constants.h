#ifndef CONSTANTS_H
#define CONSTANTS_H
#include <Arduino.h>

const int Serial_Buffer_Size = 1000;
const int Json_Message_Buffer_Size = 4000;

extern const long Baudrate;
extern const int Angle_Sensor_Pin;

extern const uint32_t Timer_Period;

extern const float Position_Gain;
extern const float Velocity_FFwd;

#endif
