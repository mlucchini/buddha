#ifndef SERVO_CONTROL_H
#define SERVO_CONTROL_H

#include "pid.h"
#include "servo_position_encoder.h"
#include "servo_arm_gravity_feed_forward.h"
#include "memory.h"

class ServoControl {
public:
  ServoControl(uint8_t zeroRawPosition);
    
  void setup();
  void update();
  void setTarget(int target);

  int getMinPwm();
  void setMinPwm(int pwm);
  int getMaxPwm();
  void setMaxPwm(int pwm);

  int getAngle();
  uint8_t getZeroRawPosition();
  void setZeroRawPosition(uint8_t rawPosition);
  uint8_t getRawPosition();

  int16_t getGravityFeedForward();
  void setGravityFeedForward(int16_t gravityFeedForward);

private:
  int getMotorDirection();
  int getMotorSpeed();

  int minPwm;
  int maxPwm;
  int target;
  double output;
  int motorGravityFeedForwardPwm;

  PID pid;
  ServoPositionEncoder servoPositionEncoder;
  ServoArmGravityFeedForward servoArmGravityFeedForward;
};

#endif
