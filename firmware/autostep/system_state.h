#ifndef SYSTEM_STATE_H
#define SYSTEM_STATE_H

#include "stepper_driver.h"
#include "message_receiver.h"
#include "em3242_angle_sensor.h"
#include "ArduinoJson.h"


class SystemState
{
    public:

        SystemState();

        void initialize();
        void process_messages();

        void update_on_timer();
        void update_on_serial_event();

    protected:

        StepperDriver stepper_driver_;
        EM3242_AngleSensor angle_sensor_;
        MessageReceiver message_receiver_;

        // Message handlers
        void handle_json_message(JsonObject &json_msg, JsonObject &json_rsp);
        void handle_json_command(JsonObject &json_msg, JsonObject &json_rsp);

        void hard_stop_command(JsonObject &json_msg, JsonObject &json_rsp);
        void soft_stop_command(JsonObject &json_msg, JsonObject &json_rsp);

        void is_busy_command(JsonObject &json_msg, JsonObject &json_rsp);
        void run_command(JsonObject &json_msg, JsonObject &json_rsp);

        void move_to_command(JsonObject &json_msg, JsonObject &json_rsp);
        void move_to_fullsteps_command(JsonObject &json_msg, JsonObject &json_rsp);
        void move_to_microsteps_command(JsonObject &json_msg, JsonObject &json_rsp);

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

};

#endif
