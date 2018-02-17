#ifndef VELOCITY_CONTROLLER_H
#define VELOCITY_CONTROLLER_H
#include "trajectory.h"
#include "stepper_driver.h"

struct UpdateInfo
{
    float error;
    float curr_position; 
    float setp_position; 
    bool done;
};

class VelocityController
{
    public:

        float DefaultPositionGain = 200.0;
        float DefaultVelocityFFwd = 1.0;

        VelocityController();

        void set_position_gain(float gain);
        float get_position_gain();

        void set_velocity_ffwd(float ffwd);
        float get_velocity_ffwd();

        UpdateInfo update(float t, StepperDriver &stepper, Trajectory &trajectory);

    protected:

        float position_gain_;
        float velocity_ffwd_;

};

#endif
