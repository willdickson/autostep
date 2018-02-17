#include "sin_trajectory.h"
#define _USE_MATH_DEFINES
#include <math.h>
#include "utility.h"


SinTrajectory::SinTrajectory(float amplitude, float period, float phase, float offset, uint32_t num_cycle)
{
    amplitude_ = amplitude;
    period_ = period;
    phase_ = deg_to_rad(phase);
    offset_ = offset;
    num_cycle_ = num_cycle;
}


float SinTrajectory::position(float t)
{
   return amplitude_*sin((2.0*M_PI/period_)*t + phase_) + offset_;
}


float SinTrajectory::velocity(float t)
{
    return (2.0*M_PI/period_)*amplitude_*cos((2.0*M_PI/period_)*t + phase_);
}


bool SinTrajectory::is_done(float t) 
{
    if (t >= period_*num_cycle_)
    {
        return true;
    }
    else
    {
        return false;
    }
}


void SinTrajectory::set_amplitude(float amplitude)
{
    amplitude_ = amplitude;
}


void SinTrajectory::set_period(float period)
{
    period_ = period;
}


void SinTrajectory::set_phase(float phase)
{
    phase_ = phase;
}


void SinTrajectory::set_offset(float offset)
{
    offset_ = offset;
}


void SinTrajectory::set_num_cycle(uint32_t num)
{
    num_cycle_ = num;
}


float SinTrajectory::amplitude()
{
    return amplitude_;
}


float SinTrajectory::period()
{
    return period_;
}


float SinTrajectory::phase()
{
    return rad_to_deg(phase_);
}


float SinTrajectory::offset()
{
    return offset_;
}


int SinTrajectory::num_cycle()
{
    return num_cycle_;
}
