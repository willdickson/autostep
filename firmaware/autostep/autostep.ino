#include "Streaming.h"
#include "ArduinoJson.h"
#include "constants.h"
#include "system_state.h"

SystemState system_state;


void setup()
{
    Serial.begin(Baudrate);
    system_state.initialize();
}



void loop()
{
    system_state.process_messages();

}


void serialEvent()
{
    system_state.update_on_serial_event();
}





// -------------------------------------------------------------------------
//
//StepperDriver stepper; 
//VelocityController controller;
//SinTrajectory trajectory(amplitude, period, phase);


//const float pos_gain = 100.0;
//const float vel_ffwd = 1.0;
//
//const float period = 4.0;
//const float amplitude = 90.0;
//const float phase = 0.5*M_PI;
//
//const long  dt_usec = 1000;
//const float dt_sec = 1.0e-6*dt_usec;

//IntervalTimer timer;
//bool timer_flag = false;
//
//void on_timer()
//{
//    timer_flag = true;
//}

//void setup()
//{
//
//    Serial.begin(115200);
//    stepper.initialize();
//
//    controller.set_position_gain(pos_gain);
//    controller.set_velocity_ffwd(vel_ffwd);
//
//    stepper.set_movement_params_to_jog();
//    stepper.move_to(trajectory.position(0.0));
//    stepper.busy_wait();
//    delay(1000);
//    stepper.set_movement_params_to_max();
//
//    timer.priority(0);
//    timer.begin(on_timer, dt_usec);
//
//    //stepper.run(100.0);
//}
//
//void loop()
//{
//    static float t = 0.0;
//    static float t_last = 0.0;
//    static UpdateInfo info;
//
//    if (timer_flag)
//    {
//        t += dt_sec;
//        info = controller.update(t,stepper,trajectory);
//        timer_flag = false;
//    }
//
//    if (t - t_last > 0.01)
//    {
//        Serial.print("c: ");
//        Serial.println(info.curr_position);
//        Serial.print("s: ");
//        Serial.println(info.setp_position);
//        Serial.print("e: ");
//        Serial.println(info.error);
//        Serial.println();
//        t_last = t;
//    }
//
//}

