#ifndef EM3242_ANGLE_SENSOR_H
#define EM3242_ANGLE_SENSOR_H
#include <Arduino.h>

class EM3242_AngleSensor
{

    public:

        static const int Default_ADC_Pin;

        static const uint16_t ADC_Averaging;
        static const uint16_t ADC_ReadResolution;
        static const uint16_t ADC_MaxValue;
        static const float Sensor_Min_Volt;
        static const float Sensor_Max_Volt;

        EM3242_AngleSensor();
        EM3242_AngleSensor(int pin);

        void initialize();
        void initialize(int pin);

        float position();
        float voltage();
        uint16_t adc_integer();

    protected:

        int pin_;
        bool invert_;
        float volt_to_degree(float volt); 

};

#endif
