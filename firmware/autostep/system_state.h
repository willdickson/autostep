#ifndef SYSTEM_STATE_H
#define SYSTEM_STATE_H

#include "stepper_driver.h"
#include "message_receiver.h"
#include "em3242_angle_sensor.h"

#include "trajectory.h"
#include "sin_trajectory.h"
#include "velocity_controller.h"
#include "ArduinoJson.h"


struct MoveModeParams 
{
    float speed;
    float acceleration;
    float deceleration;
};



class SystemState
{
    public:

        SystemState();

        void initialize();
        void set_timer_callback(void(*func)());
        void process_messages();

        void update_trajectory();
        void update_on_timer();
        void update_on_serial_event();

    protected:

        MessageReceiver message_receiver_;

        StepperDriver stepper_driver_;
        EM3242_AngleSensor angle_sensor_;

        VelocityController velocity_controller_;

        volatile bool timer_flag_;
        IntervalTimer interval_timer_;

        static void dummy_callback_() {};
        void (*timer_callback_)() = dummy_callback_;

        float time_sec_;

        float data_send_dt_;
        float time_last_send_sec_;

        Trajectory *trajectory_ptr_;
        SinTrajectory sin_trajectory_;
        void start_trajectory();
        bool is_trajectory_running();

        // Message handlers
        void handle_json_message(JsonObject &json_msg, JsonObject &json_rsp);
        void handle_json_command(JsonObject &json_msg, JsonObject &json_rsp);

        void hard_stop_command(JsonObject &json_msg, JsonObject &json_rsp);
        void soft_stop_command(JsonObject &json_msg, JsonObject &json_rsp);

        void is_busy_command(JsonObject &json_msg, JsonObject &json_rsp);

        void move_to_command(JsonObject &json_msg, JsonObject &json_rsp);
        void move_to_fullsteps_command(JsonObject &json_msg, JsonObject &json_rsp);
        void move_to_microsteps_command(JsonObject &json_msg, JsonObject &json_rsp);

        void run_command(JsonObject &json_msg, JsonObject &json_rsp);
        void sinusoid_command(JsonObject &json_msg, JsonObject &json_rsp);

        void get_position_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_position_command(JsonObject &json_msg, JsonObject &json_rsp);

        void get_position_fullsteps_command(JsonObject &json_msg, JsonObject &json_rsp);
        void get_position_microsteps_command(JsonObject &json_msg, JsonObject &json_rsp);

        void get_position_sensor_command(JsonObject &json_msg, JsonObject &json_rsp);
        void get_voltage_sensor_command(JsonObject &json_msg, JsonObject &json_rsp);
        void autoset_position_command(JsonObject &json_msg, JsonObject &json_rsp);

        void set_jog_mode_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_max_mode_command(JsonObject &json_msg, JsonObject &json_rsp);

        void enable_command(JsonObject &json_msg, JsonObject &json_rsp);
        void release_command(JsonObject &json_msg, JsonObject &json_rsp);

        void get_step_mode_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_step_mode_command(JsonObject &json_msg, JsonObject &json_rsp);

        void get_fullstep_per_rev_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_fullstep_per_rev_command(JsonObject &json_msg, JsonObject &json_rsp);

        MoveModeParams get_move_mode_params(JsonObject &json_msg, JsonObject &json_rsp);
        void get_jog_mode_params_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_jog_mode_params_command(JsonObject &json_msg, JsonObject &json_rsp);
        void get_max_mode_params_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_max_mode_params_command(JsonObject &json_msg, JsonObject &json_rsp);

        void get_kval_params_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_kval_params_command(JsonObject &json_msg, JsonObject &json_rsp);

        void get_oc_threshold_command(JsonObject &json_msg, JsonObject &json_rsp);
        void set_oc_threshold_command(JsonObject &json_msg, JsonObject &json_rsp);

};

#endif
