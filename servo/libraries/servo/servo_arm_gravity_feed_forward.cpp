#include <Arduino.h>

#include "servo_arm_gravity_feed_forward.h"

/**
 * Returns between 0 (moving down or vertical arm) and 1 (moving up and horizontal arm)
 */
double ServoArmGravityFeedForward::getProportion(double actual, double setpoint) {
  if (! this->isAgainstGravity(actual, setpoint)) return 0;
  return sin(abs(actual) * PI / 180);
}

bool ServoArmGravityFeedForward::areSameSign(double a, double b) {
  return (a >= 0 && b >= 0) || (a < 0 && b < 0);
}

bool ServoArmGravityFeedForward::isAgainstGravity(double actual, double setpoint) {
  return areSameSign(actual, setpoint) && abs(setpoint) > abs(actual);
}
