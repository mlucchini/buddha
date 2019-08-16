#ifndef COMMANDS_HANDLER_H
#define COMMANDS_HANDLER_H

#include "serial_io.h"
#include "serial_connection.h"
#include "servo_control.h"
#include "memory.h"

class CommandsHandler {
public:
  CommandsHandler(SerialConnection &serialConnection, ServoControl &servoControl, Memory &memory);

  void handle();

private:
  void defaultHandler(Order order);
  void helloHandler();
  void getServoAngleHandler();
  void setServoAngleHandler();
  void getIdentifierHandler();
  void setIdentifierHandler();
  void getMinPwm();
  void setMinPwm();
  void getMaxPwm();
  void setMaxPwm();
  void getZeroRawPosition();
  void setZeroRawPosition();
  void getGravityFeedForward();
  void setGravityFeedForward();

  SerialConnection &serialConnection;
  ServoControl &servoControl;
  Memory &memory;
};

#endif
