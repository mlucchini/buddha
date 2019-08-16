#ifndef SERVO_POSITION_ENCODER_H
#define SERVO_POSITION_ENCODER_H

#include <ACE128.h>

class ServoPositionEncoder {
public:
  ServoPositionEncoder(uint8_t zeroRawPosition);

  void setup();
  void update();

  int getAngle();
  uint8_t getRawPosition();
  uint8_t getZeroRawPosition();
  void setZeroRawPosition(uint8_t rawPosition);

private:
  ACE128 ace;
  uint8_t pinPos;
  uint8_t oldPos;
  uint8_t zeroRawPosition;
  int angle;
};

#endif
