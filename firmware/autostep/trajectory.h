#ifndef TRAJECTORY_H
#define TRAJECTORY_H


class Trajectory
{
    public:

        Trajectory();
        virtual float position(float t);
        virtual float velocity(float t);

        bool is_running();

    protected:

        bool running_;
};


#endif
