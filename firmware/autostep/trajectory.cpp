#include "trajectory.h"


Trajectory::Trajectory() 
{
    running_ = false;
}

bool Trajectory::is_running()
{
    return running_;
}


float Trajectory::position(float t)
{ 
    return 0.0;
}


float Trajectory::velocity(float t) 
{
    return 0.0;
}
