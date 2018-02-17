#include "trajectory.h"


Trajectory::Trajectory() 
{}

float Trajectory::position(float t)
{ 
    return 0.0;
}


float Trajectory::velocity(float t) 
{
    return 0.0;
}

bool Trajectory::is_done(float t)
{
    return true;

}

Trajectory::Status Trajectory::status()
{
    return status_;
}

void Trajectory::set_status(Trajectory::Status value)
{
    status_ = value;
}
