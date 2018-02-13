#include "sin_trajectory.h"
#define _USE_MATH_DEFINES
#include <math.h>


SinTrajectory::SinTrajectory(float amplitude, float period, float phase)
{
    amplitude_ = amplitude;
    period_ = period;
    phase_ = phase;
}

float SinTrajectory::position(float t)
{
   return amplitude_*sin((2.0*M_PI/period_)*t + phase_);
}


float SinTrajectory::velocity(float t)
{
    return (2.0*M_PI/period_)*amplitude_*cos((2.0*M_PI/period_)*t + phase_);
}
