#include "em3242_angle_sensor.h"

const int EM3242_AngleSensor::Default_ADC_Pin = A1;
const uint16_t EM3242_AngleSensor::ADC_Averaging = 16;
const uint16_t EM3242_AngleSensor::ADC_ReadResolution = 16;
const uint16_t EM3242_AngleSensor::ADC_MaxValue = uint16_t((uint32_t(1) << ADC_ReadResolution) -1);
const float EM3242_AngleSensor::Sensor_Min_Volt = 0.1;
const float EM3242_AngleSensor::Sensor_Max_Volt = 0.9;


EM3242_AngleSensor::EM3242_AngleSensor() : EM3242_AngleSensor(Default_ADC_Pin)
{}


EM3242_AngleSensor::EM3242_AngleSensor(int pin)
{
    pin_ = pin;
    invert_ = true;
}


void EM3242_AngleSensor::initialize()
{
    analogReadResolution(ADC_ReadResolution);
    analogReadAveraging(ADC_Averaging);
    pinMode(pin_,INPUT);
}


void EM3242_AngleSensor::initialize(int pin)
{
    pin_ = pin;
    initialize();
}


float EM3242_AngleSensor::position()
{
    float position = volt_to_degree(voltage());
    if (invert_)
    {
        position = 360.0 - position;
    }
    return position;
}


float EM3242_AngleSensor::voltage()
{
    return float(adc_integer())/float(ADC_MaxValue);
}


uint16_t EM3242_AngleSensor::adc_integer()
{
    return analogRead(pin_);
}


float EM3242_AngleSensor::volt_to_degree(float volt) 
{
    float A = 360.0/(Sensor_Max_Volt-Sensor_Min_Volt);
    float B = -Sensor_Min_Volt*A;
    return A*volt + B;
}
