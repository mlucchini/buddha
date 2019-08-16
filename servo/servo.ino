#include <serial_parameters.h>
#include <serial_order.h>
#include <serial_io.h>
#include <serial_connection.h>
#include <servo_control.h>
#include <commands_handler.h>
#include <memory.h>

SerialConnection serialConnection;
Memory memory;
ServoControl servoControl(memory.getZeroRawPosition());
CommandsHandler commandsHandler(serialConnection, servoControl, memory);

void serialEvent() {
  commandsHandler.handle();
}

void setup() {
  servoControl.setup();
  Serial.begin(SERIAL_BAUD);
}

void loop() {
  if (serialConnection.isConnected()) {
    servoControl.update();
  }
}
