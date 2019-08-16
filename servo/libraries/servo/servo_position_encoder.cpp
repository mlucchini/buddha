#include <ACE128.h>
#include <ACE128map12345678.h>

#include "servo_position_encoder.h"
#include "servo_parameters.h"
#include "serial_io.h"

ServoPositionEncoder::ServoPositionEncoder(uint8_t zeroRawPosition)
  : ace(ACE_INPUT_PIN_1, ACE_INPUT_PIN_2, ACE_INPUT_PIN_3, ACE_INPUT_PIN_4, ACE_INPUT_PIN_5, ACE_INPUT_PIN_6, ACE_INPUT_PIN_7, ACE_INPUT_PIN_8, (uint8_t*) encoderMap_12345678)
  , pinPos(0)
  , oldPos(255)
  , zeroRawPosition(zeroRawPosition) {
}

void ServoPositionEncoder::setup() {
  this->ace.begin();
  this->ace.setZero(this->zeroRawPosition);
  this->update();
}

void ServoPositionEncoder::update() {
  this->pinPos = this->ace.acePins();

  // Multi-turn position is convenient since the target can be overshot
  int8_t pos = this->ace.mpos();
  if (this->pinPos != this->oldPos) {
    this->oldPos = this->pinPos;
    this->angle = map(pos, -ACE_CPR / 2, ACE_CPR / 2, -MOTOR_MAX_ROTATION / 2, MOTOR_MAX_ROTATION / 2);
    println("Sensor: " + String(this->angle));
  }
}

int ServoPositionEncoder::getAngle() {
  return this->angle;
}

uint8_t ServoPositionEncoder::getRawPosition() {
  return this->ace.rawPos();
}

uint8_t ServoPositionEncoder::getZeroRawPosition() {
  return this->ace.getZero();
}

void ServoPositionEncoder::setZeroRawPosition(uint8_t rawPosition) {
  this->zeroRawPosition = rawPosition;
  this->setup();
}
