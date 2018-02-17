#ifndef TRAJECTORY_H
#define TRAJECTORY_H


class Trajectory
{
    public:

        enum Status {Setup,Running,Done};

        Trajectory();
        virtual float position(float t);
        virtual float velocity(float t);
        virtual bool is_done(float t);

        Trajectory::Status status();
        void set_status(Trajectory::Status value);

    protected:

        Status status_;


};


#endif
