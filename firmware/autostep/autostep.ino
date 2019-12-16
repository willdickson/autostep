#include "Streaming.h"
#include "ArduinoJson.h"
#include "constants.h"
#include "system_state.h"

SystemState system_state;


void setup()
{
    Serial.begin(Baudrate);
    system_state.initialize();
    system_state.set_timer_callback(timerEvent);
}


void loop()
{
    system_state.update_homing();
    system_state.update_trajectory();
    system_state.process_messages();
}


void timerEvent()
{
    system_state.update_on_timer();
}


void serialEvent()
{
    system_state.update_on_serial_event();
}




