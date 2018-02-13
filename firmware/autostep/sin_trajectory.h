#ifndef SIN_TRAJECTORY_H
#define SIN_TRAJECTORY_H
#include "trajectory.h"

class SinTrajectory : public Trajectory
{
    public:
        
        SinTrajectory(float amplitude=1.0, float period=1.0, float phase=0.0);
        virtual float position(float t) override;
        virtual float velocity(float t) override;

    protected:

        float amplitude_;
        float period_;
        float phase_;

};

#endif 
