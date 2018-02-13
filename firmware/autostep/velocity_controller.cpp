#include "velocity_controller.h"


VelocityController::VelocityController()
{ 
    position_gain_ = DefaultPositionGain;
    velocity_ffwd_ = DefaultVelocityFFwd;
}


void VelocityController::set_position_gain(float gain)
{
    position_gain_ = gain;
}


float VelocityController::get_position_gain()
{
    return position_gain_;
}


void VelocityController::set_velocity_ffwd(float ffwd)
{
    velocity_ffwd_ = ffwd;
}


float VelocityController::get_velocity_ffwd()
{
    return velocity_ffwd_;
}


UpdateInfo VelocityController::update(float t, StepperDriver &stepper, Trajectory &trajectory)
{
    float curr_position = stepper.get_position();
    float setp_position = trajectory.position(t);
    float setp_velocity = trajectory.velocity(t);
    float error = setp_position - curr_position;
    float next_velocity = position_gain_*(setp_position - curr_position) + velocity_ffwd_*setp_velocity;
    stepper.run(next_velocity);
    UpdateInfo info = {error, curr_position, setp_position};
    return info;
}

