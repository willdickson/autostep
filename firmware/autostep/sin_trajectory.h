#ifndef SIN_TRAJECTORY_H
#define SIN_TRAJECTORY_H
#include "trajectory.h"
#include <Arduino.h>

class SinTrajectory : public Trajectory
{
    public:
        
        SinTrajectory(float amplitude=1.0, float period=1.0, float phase=0.0, float offset=0.0, uint32_t num_cycle=1);

        virtual float position(float t) override;
        virtual float velocity(float t) override;
        virtual bool is_done(float t) override;

        void set_amplitude(float amplitude);
        void set_period(float period);
        void set_phase(float phase);
        void set_offset(float offset);
        void set_num_cycle(uint32_t num);

        float amplitude();
        float period();
        float phase();
        float offset();
        int num_cycle();

    protected:

        float amplitude_;
        float period_;
        float phase_;
        float offset_;
        uint32_t num_cycle_;

};

#endif 
