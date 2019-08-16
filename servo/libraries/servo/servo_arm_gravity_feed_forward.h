#ifndef SERVO_ARM_GRAVITY_FEED_FORWARD_H
#define SERVO_ARM_GRAVITY_FEED_FORWARD_H


class ServoArmGravityFeedForward {
public:
  double getProportion(double actual, double setpoint);

private:
  bool areSameSign(double a, double b);
  bool isAgainstGravity(double actual, double setpoint);
};


#endif
