#include "system_state.h"
#include "Streaming.h"


// Public methods
// ------------------------------------------------------------------------------------------------

SystemState::SystemState() {}


void SystemState::initialize() 
{
    stepper_driver_.initialize();
    stepper_driver_.set_movement_params_to_jog();
    stepper_driver_.enable();
    angle_sensor_.initialize(Angle_Sensor_Pin);
    message_receiver_.reset();

    curr_trajectory_ptr_ = nullptr;
    timer_callback_ = nullptr;

    t_sec_ = 0.0;
}


void SystemState::set_timer_callback(void(*callback)())
{
    if (callback != nullptr)
    {
        timer_callback_ = callback; 
    }
}


void SystemState::process_messages()
{
    if (message_receiver_.available())
    {
        String message = message_receiver_.next();

        StaticJsonBuffer<Json_Message_Buffer_Size> json_msg_buffer;
        StaticJsonBuffer<Json_Message_Buffer_Size> json_rsp_buffer;

        JsonObject &json_msg = json_msg_buffer.parse(message);
        JsonObject &json_rsp = json_rsp_buffer.createObject();

        if (json_msg.success())
        {
            handle_json_message(json_msg, json_rsp);
        }
        else
        {
            json_rsp["success"] = false;
            json_rsp["message"] = "parse error";
        }
        json_rsp.printTo(Serial);
        Serial << endl;
    }
}


void SystemState::update_on_timer()
{

}


void SystemState::update_on_serial_event()
{
    message_receiver_.read_data();

}


// Protected methods
// ------------------------------------------------------------------------------------------------

void SystemState::handle_json_message(JsonObject &json_msg, JsonObject &json_rsp)
{
    if (json_msg.containsKey("command"))
    {
        handle_json_command(json_msg, json_rsp);
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "command missing";
    }
}


void SystemState::handle_json_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    String command = String((const char*)(json_msg["command"]));

    //Serial << "command = " << command << endl;

    // Command switchyard
    // --------------------------------------------------------------------------
    if (command.equals("hard_stop"))
    {
        hard_stop_command(json_msg, json_rsp);
    }
    else if (command.equals("soft_stop"))
    {
        soft_stop_command(json_msg, json_rsp);
    }
    else if (command.equals("is_busy"))
    {
        is_busy_command(json_msg, json_rsp);
    }
    else if (command.equals("move_to"))
    {
        move_to_command(json_msg, json_rsp);
    }
    else if (command.equals("move_to_fullsteps"))
    {
        move_to_fullsteps_command(json_msg, json_rsp);
    }
    else if (command.equals("move_to_microsteps"))
    {
        move_to_microsteps_command(json_msg, json_rsp);
    }
    else if (command.equals("run"))
    {
        run_command(json_msg, json_rsp);
    }
    else if (command.equals("sinusoid"))
    {
        sinusoid_command(json_msg, json_rsp);
    }
    else if (command.equals("get_position"))
    {
        get_position_command(json_msg, json_rsp);
    }
    else if (command.equals("set_position"))
    {
        set_position_command(json_msg, json_rsp);
    }
    else if (command.equals("get_position_fullsteps"))
    {
        get_position_fullsteps_command(json_msg, json_rsp);
    }
    else if (command.equals("get_position_microsteps"))
    {
        get_position_microsteps_command(json_msg, json_rsp);
    }
    else if (command.equals("get_position_sensor"))
    {
        get_position_sensor_command(json_msg, json_rsp);
    }
    else if (command.equals("get_voltage_sensor"))
    {
        get_voltage_sensor_command(json_msg, json_rsp);
    }
    else if (command.equals("autoset_position"))
    {
        autoset_position_command(json_msg, json_rsp);
    }
    else if (command.equals("set_jog_mode"))
    {
        set_jog_mode_command(json_msg, json_rsp);
    }
    else if(command.equals("set_max_mode"))
    {
        set_max_mode_command(json_msg, json_rsp);
    }
    else if (command.equals("enable"))
    {
        enable_command(json_msg, json_rsp);
    }
    else if (command.equals("release"))
    {
        release_command(json_msg, json_rsp);
    }
    else if (command.equals("get_step_mode"))
    {
        get_step_mode_command(json_msg, json_rsp);
    }
    else if (command.equals("set_step_mode"))
    {
        set_step_mode_command(json_msg, json_rsp);
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = String("unknown command: ") + command;
    }
}


void SystemState::hard_stop_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    stepper_driver_.hard_stop();
    json_rsp["success"] = true;
}


void SystemState::soft_stop_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    stepper_driver_.soft_stop();
    json_rsp["success"] = true;
}

void SystemState::is_busy_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    bool is_busy = stepper_driver_.is_busy();
    json_rsp["success"] = true;
    json_rsp["is_busy"] = is_busy;
}




void SystemState::move_to_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    if (json_msg.containsKey("position"))
    {
        float position = json_msg["position"];
        stepper_driver_.move_to(position);
        json_rsp["success"] = true;
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing position";
    }
}


void SystemState::move_to_fullsteps_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    if (json_msg.containsKey("position"))
    {
        float position = json_msg["position"];
        stepper_driver_.move_to_fullsteps(position);
        json_rsp["success"] = true;
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing position";
    }
}


void SystemState::move_to_microsteps_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    if (json_msg.containsKey("position"))
    {
        long position = json_msg["position"];
        stepper_driver_.move_to_microsteps(position);
        json_rsp["success"] = true;
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing position";
    }
}

void SystemState::run_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    if (json_msg.containsKey("velocity"))
    {
        float velocity = json_msg["velocity"];
        stepper_driver_.run(velocity);
        json_rsp["success"] = true;
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing velocity";
    }
}


void SystemState::sinusoid_command(JsonObject &json_msg, JsonObject &json_rsp)
{ 

    if (json_msg.containsKey("amplitude"))
    {
        sin_trajectory_.set_amplitude(json_msg["amplitude"]);
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing amplitude";
        return;
    }


    if (json_msg.containsKey("period"))
    {
        sin_trajectory_.set_period(json_msg["period"]);
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing period";
        return;
    }

   
    if (json_msg.containsKey("offset"))
    {
        sin_trajectory_.set_offset(json_msg["offset"]);
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing offset";
        return;
    }

    if (json_msg.containsKey("phase"))
    {
        sin_trajectory_.set_phase(json_msg["phase"]);
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing phase";
        return;
    }

    if (json_msg.containsKey("num_cycle"))
    {
        float num_cycle = json_msg["num_cycle"];
        sin_trajectory_.set_num_cycle(uint32_t(num_cycle));
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing num_cycles";
        return;
    }


    curr_trajectory_ptr_ = &sin_trajectory_;

    json_rsp["success"] = true;
    json_rsp["amplitude"] = sin_trajectory_.amplitude();
    json_rsp["period"] = sin_trajectory_.period();
    json_rsp["phase"] = sin_trajectory_.phase();
    json_rsp["offset"] = sin_trajectory_.offset();
    json_rsp["num_cycle"] = sin_trajectory_.num_cycle();
}


void SystemState::get_position_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    float position = stepper_driver_.get_position();
    json_rsp["success"] = true;
    json_rsp["position"] = position;
}


void SystemState::set_position_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    if (json_msg.containsKey("position"))
    {
        float position = json_msg["position"];
        stepper_driver_.set_position(position);
        json_rsp["success"] = true;
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing position";
    }
}


void SystemState::get_position_fullsteps_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    float position_fullsteps = stepper_driver_.get_position_fullsteps();
    json_rsp["success"] = true;
    json_rsp["position"] = position_fullsteps;
}


void SystemState::get_position_microsteps_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    long position_microsteps = stepper_driver_.get_position_microsteps();
    json_rsp["success"] = true;
    json_rsp["position"] = position_microsteps;
}


void SystemState::get_position_sensor_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    float position = angle_sensor_.position();
    json_rsp["success"] = true;
    json_rsp["position"] = position;
}


void SystemState::get_voltage_sensor_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    float voltage = angle_sensor_.voltage();
    json_rsp["success"] = true;
    json_rsp["voltage"] = voltage;
}


void SystemState::autoset_position_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    stepper_driver_.set_position(angle_sensor_.position());
    json_rsp["success"] = true;
}

void SystemState::set_jog_mode_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    stepper_driver_.set_movement_params_to_jog();
    json_rsp["success"] = true;
}


void SystemState::set_max_mode_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    stepper_driver_.set_movement_params_to_max();
    json_rsp["success"] = true;
}


void SystemState::enable_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    stepper_driver_.enable();
    json_rsp["success"] = true;
}


void SystemState::release_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    stepper_driver_.release();
    json_rsp["success"] = true;
}


void SystemState::get_step_mode_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    String step_mode_string = stepper_driver_.get_step_mode_string();
    json_rsp["success"] = true;
    json_rsp["step_mode"] = step_mode_string;
}

void SystemState::set_step_mode_command(JsonObject &json_msg, JsonObject &json_rsp)
{
    if (json_msg.containsKey("step_mode"))
    {

        String step_mode_string = json_msg["step_mode"];

        // Get current enabled state
        bool is_enabled = stepper_driver_.is_enabled();
        stepper_driver_.release();  // Required

        bool ok = stepper_driver_.set_step_mode(step_mode_string);

        if (ok)
        {
            json_rsp["success"] = true;
        }
        else
        {
            json_rsp["success"] = false;
            json_rsp["message"] = String("failed to set mode to ") + step_mode_string;
        }

        if (is_enabled)
        {
            stepper_driver_.enable();
        }
    }
    else
    {
        json_rsp["success"] = false;
        json_rsp["message"] = "missing step_mode";
    }
}




