#include <Arduino.h>

#include "servo_control.h"
#include "servo_parameters.h"
#include "serial_io.h"

ServoControl::ServoControl(uint8_t zeroRawPosition)
  : minPwm(MOTOR_MIN_PWM)
  , maxPwm(MOTOR_MAX_PWM)
  , target(0)
  , output(0.0)
  , motorGravityFeedForwardPwm(MOTOR_GRAVITY_FEED_FORWARD_PWM)
  , pid(PID_P, PID_I, PID_D, PID_F)
  , servoPositionEncoder(zeroRawPosition) {
}

void ServoControl::setup() {
  pinMode(MOTOR_A1_OUTPUT_PIN, OUTPUT);
  pinMode(MOTOR_B1_OUTPUT_PIN, OUTPUT);
  pinMode(PWM_MOTOR_OUTPUT_PIN, OUTPUT);

  this->servoPositionEncoder.setup();

  this->target = this->servoPositionEncoder.getAngle();
  this->pid.setOutputLimits(-MOTOR_MAX_ROTATION / 2, MOTOR_MAX_ROTATION / 2);
  this->pid.setDeadBandWindow(DEAD_BAND_WINDOW);
}

void ServoControl::setTarget(int target) {
  this->target = constrain(target, -MOTOR_MAX_ROTATION / 2, MOTOR_MAX_ROTATION / 2);
}

int ServoControl::getMinPwm() {
  return this->minPwm;
}

void ServoControl::setMinPwm(int pwm) {
  this->minPwm = constrain(pwm, 0, this->maxPwm);
}

int ServoControl::getMaxPwm() {
  return this->maxPwm;
}

void ServoControl::setMaxPwm(int pwm) {
  this->maxPwm = constrain(pwm, this->minPwm, 255);
}

void ServoControl::update() {
  servoPositionEncoder.update();

  double updatedOutput = this->pid.getOutput(servoPositionEncoder.getAngle(), target);
  if (updatedOutput != this->output) {
    this->output = updatedOutput;

    println("PID Output: " + String(output));
    println("Motor PWM: " + String(getMotorSpeed()));
    println("Motor PWM Output PIN: " + String(analogRead(PWM_MOTOR_OUTPUT_PIN)));

    if (getMotorDirection() == MOTOR_STATE_CCW) {
      digitalWrite(MOTOR_A1_OUTPUT_PIN, LOW);
      digitalWrite(MOTOR_B1_OUTPUT_PIN, HIGH);
    } else if (getMotorDirection() == MOTOR_STATE_CW) {
      digitalWrite(MOTOR_A1_OUTPUT_PIN, HIGH);
      digitalWrite(MOTOR_B1_OUTPUT_PIN, LOW);
    } else {
      digitalWrite(MOTOR_A1_OUTPUT_PIN, LOW);
      digitalWrite(MOTOR_B1_OUTPUT_PIN, LOW);
    }
    analogWrite(PWM_MOTOR_OUTPUT_PIN, getMotorSpeed());
  }
}

int ServoControl::getMotorSpeed() {
  if (this->output == 0) return 0;

  double gravityProportionFeedForward = servoArmGravityFeedForward.getProportion(servoPositionEncoder.getAngle(), target);
  int minPwm = constrain(this->minPwm + gravityProportionFeedForward * this->motorGravityFeedForwardPwm, MOTOR_MIN_PWM, MOTOR_MAX_PWM);

  return map(abs(this->output), 0, MOTOR_MAX_ROTATION / 2, minPwm, this->maxPwm);
}

int ServoControl::getMotorDirection() {
  if (this->output < 0) return MOTOR_STATE_CCW;
  if (this->output > 0) return MOTOR_STATE_CW;
  return MOTOR_STATE_BRAKE;
}

int ServoControl::getAngle() {
  return this->servoPositionEncoder.getAngle();
}

uint8_t ServoControl::getZeroRawPosition() {
  return this->servoPositionEncoder.getZeroRawPosition();
}

void ServoControl::setZeroRawPosition(uint8_t rawPosition) {
  this->servoPositionEncoder.setZeroRawPosition(rawPosition);
}

uint8_t ServoControl::getRawPosition() {
  return this->servoPositionEncoder.getRawPosition();
}

int16_t ServoControl::getGravityFeedForward() {
  return this->motorGravityFeedForwardPwm;
}

void ServoControl::setGravityFeedForward(int16_t gravityFeedForward) {
  this->motorGravityFeedForwardPwm = constrain(gravityFeedForward, 0, MOTOR_MAX_PWM);
}
