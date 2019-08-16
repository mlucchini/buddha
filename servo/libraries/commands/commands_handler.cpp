#include "commands_handler.h"

CommandsHandler::CommandsHandler(SerialConnection &serialConnection, ServoControl &servoControl, Memory &memory)
  : serialConnection(serialConnection)
  , servoControl(servoControl)
  , memory(memory) {
}

void CommandsHandler::handle() {
  if (Serial.available() > 0) {
    Order order = read_order();
    switch(order) {
      case HELLO: helloHandler(); break;
      case GET_SERVO_ANGLE: getServoAngleHandler(); break;
      case SET_SERVO_ANGLE: setServoAngleHandler(); break;
      case GET_IDENTIFIER: getIdentifierHandler(); break;
      case SET_IDENTIFIER: setIdentifierHandler(); break;
      case GET_MIN_PWM: getMinPwm(); break;
      case SET_MIN_PWM: setMinPwm(); break;
      case GET_MAX_PWM: getMaxPwm(); break;
      case SET_MAX_PWM: setMaxPwm(); break;
      case GET_ZERO_RAW_POSITION: getZeroRawPosition(); break;
      case SET_ZERO_RAW_POSITION: setZeroRawPosition(); break;
      case GET_GRAVITY_FEED_FORWARD: getGravityFeedForward(); break;
      case SET_GRAVITY_FEED_FORWARD: setGravityFeedForward(); break;
      default: defaultHandler(order); break;
    }
    write_order(RECEIVED);
  }
}

void CommandsHandler::defaultHandler(Order order) {
  println("Received unrecognized order");

  write_order(ERROR);
  write_order(order);
}

void CommandsHandler::helloHandler() {
  println("Received order HELLO");

  this->serialConnection.setConnected();
  write_order(CONNECTED);
}

void CommandsHandler::getServoAngleHandler() {
  println("Received order GET_SERVO_ANGLE");

  write_i16(servoControl.getAngle());
}

void CommandsHandler::setServoAngleHandler() {
  println("Received order SET_SERVO_ANGLE");

  servoControl.setTarget(read_i16());
}

void CommandsHandler::getIdentifierHandler() {
  println("Received order GET_IDENTIFIER");

  write_i8(memory.getIdentifier());
}

void CommandsHandler::setIdentifierHandler() {
  println("Received order SET_IDENTIFIER");

  memory.setIdentifier(read_i8());
}

void CommandsHandler::getMinPwm() {
  println("Received order GET_MIN_PWM");

  write_i16(servoControl.getMinPwm());
}

void CommandsHandler::setMinPwm() {
  println("Received order SET_MIN_PWM");

  servoControl.setMinPwm(read_i16());
}

void CommandsHandler::getMaxPwm() {
  println("Received order GET_MAX_PWM");

  write_i16(servoControl.getMaxPwm());
}

void CommandsHandler::setMaxPwm() {
  println("Received order SET_MAX_PWM");

  servoControl.setMaxPwm(read_i16());
}

void CommandsHandler::getZeroRawPosition() {
  println("Received order GET_ZERO_RAW_POSITION");

  write_i8(servoControl.getZeroRawPosition());
}

void CommandsHandler::setZeroRawPosition() {
  println("Received order SET_ZERO_RAW_POSITION");

  uint8_t rawPosition = servoControl.getRawPosition();
  memory.setZeroRawPosition(rawPosition);
  servoControl.setZeroRawPosition(rawPosition);
}

void CommandsHandler::getGravityFeedForward() {
  println("Received order GET_GRAVITY_FEED_FORWARD");

  write_i16(servoControl.getGravityFeedForward());
}

void CommandsHandler::setGravityFeedForward() {
  println("Received order SET_GRAVITY_FEED_FORWARD");

  servoControl.setGravityFeedForward(read_i16());
}
