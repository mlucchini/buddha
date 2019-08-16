/*
  Exercise Monster Motor Mini Module
  Uses Serial Monitor window to issue commands for controlling the DC motor
  connected to the module
  S = Stop
  F = Forward
  R = Reverse
  C = Returns the current reading of the motors
  Pxxx (P0 - P255) sets the PWM speed value
  P? = Returns the current PWM value

  ACE PIN Serial Tester
  This displays the current position in all five forms on the serial monitor
     pin = the raw gray-code from the pins. As you rotate this will rise and fall in steps
           of 1,2,4,8,16,32,64 or 128
     raw = the output from the encoder map table. This should rise from 0 - 127 as you rotate clockwise
           if it jumps around and shows 255 a lot - your wiring does not match your encode map. Check your wiring
           and your object declaration. See the make_encodermap example sketch to create encoder maps for
           alternate pin arrangements
     pos = this is the raw value converted to the range -64 - +63 relative to the logical zero. Logical zero is
           wherever it was when the sketch started, or wherever it was when pin 13 was last grounded.
     upos = this is the raw value converted to the range 0 - 127 relative to the logical zero
     mpos = this is like pos, but goes multiturn -32768 - 32767
*/

#include <ACE128.h>
#include <ACE128map12345678.h>
#include <Wire.h>

// Motor
const int BRAKE = 0;
const int CW = 1;
const int CCW = 2;
const int CS_THRESHOLD = 15;
const int MOTOR_A1_PIN = 12;   // Motor control input pins
const int MOTOR_B1_PIN = 11;
const int PWM_MOTOR_PIN = 10;  // Motor PWM input pin
const int CURRENT_SENSE = A2;  // Current sense pin
const int EN_PIN = A0;         // Enable pin
int motorSpeed = 75;           // Default motor speed
int motorState = BRAKE;        // Current motor state
int motorCurrent = 0;          // Motor current
char readString[4];            // String array to hold PWM value typed in on keyboard

// Encoder
ACE128 myACE(2,3,4,5,6,7,8,9, (uint8_t*) encoderMap_12345678);
const int ZERO = 13;
uint8_t pinPos = 0;
uint8_t rawPos = 0;
uint8_t upos = 0;
uint8_t oldPos = 255;
int8_t pos;
int16_t mpos;
uint8_t seen = 0;

void setup() {
  pinMode(MOTOR_A1_PIN, OUTPUT);
  pinMode(MOTOR_B1_PIN, OUTPUT);
  pinMode(PWM_MOTOR_PIN, OUTPUT);

  int error = 1;
  myACE.begin();
  pinMode(ZERO, INPUT_PULLUP);
  pinPos = myACE.acePins();
  oldPos = pinPos;
  Serial.begin(9600);
  Serial.println(myACE.acePins());

  Serial.begin(9600);
  Serial.println("Enter command:");
  Serial.println("S = STOP");
  Serial.println("F = FORWARD");
  Serial.println("R = REVERSE");
  Serial.println("C = READ MOTOR CURRENT");
  Serial.println("Pxxx = PWM SPEED (P000 - P254)");
  Serial.println("P? = RETURNS CURRENT PWM SPEED");
}

void loop() {
  if (Serial.available()) doSerial();
  doEncoder();
}

void doSerial() {
  int index = 0;
  int pwmValue = 0;
  int motor1AmpDC = 0;
  float motor1Voltage = 0.0;

  char ch = Serial.read();
  Serial.println(ch);

  switch (ch) {
    case 'f':
    case 'F':
      motorState = CW;
      motorCmd(motorState, motorSpeed);
      Serial.println("Motor Forward");
      break;

    case 'r':
    case 'R':
      motorState = CCW;
      motorCmd(motorState, motorSpeed);
      Serial.println("Motor Reverse");
      break;

    case 's':
    case 'S':
      motorState = BRAKE;
      motorCmd(motorState, 0);
      Serial.println("Motor Stop");
      break;

    case 'c':
    case 'C':
      motor1AmpDC = analogRead(CURRENT_SENSE);
      motor1Voltage = motor1AmpDC * (5.0 / 1024);
      Serial.print("Motor 1 Current: ");
      Serial.print (motor1Voltage * 26 * 100);
      Serial.println (" mA");
      break;

    case 'p':
    case 'P':
      delay(2);
      for (int i; i<4; i++) readString[i] = ' ';
      while (Serial.available()) {
        char c = Serial.read();
        readString[index] = c;
        index++;
        delay(2);
      }
      readString[3] = '\0';
      index = 0;
      if (readString[index] == '?') {
        Serial.print("Current PWM Setting: ");
        Serial.println(motorSpeed);
        break;
      }
      pwmValue = atoi(readString);
      if(pwmValue != 0) {
        if (pwmValue > 255) pwmValue = 255;
        Serial.println(pwmValue);
        motorSpeed = pwmValue;
        motorCmd(motorState, motorSpeed);
      }
      break;

    default:
      break;
  }
}

void doEncoder() {
  pinPos = myACE.acePins();
  rawPos = myACE.rawPos();
  pos = myACE.pos();
  upos = myACE.upos();
  mpos = myACE.mpos();
  if (pinPos != oldPos) {
    seen |= pinPos ^ oldPos;
    oldPos = pinPos;
    if (seen < 255) {
      Serial.println("looking for pins");
      for (uint8_t i = 0; i <= 7; i++) {
        if (! (seen & 1 << i)) {
          Serial.print(i, DEC);
        }
      }
      Serial.println("");
    } else {
      Serial.print("pin ");
      Serial.print(pinPos);
      Serial.print(" raw ");
      Serial.print(rawPos);
      Serial.print(" pos ");
      Serial.print(pos, DEC);
      Serial.print(" upos ");
      Serial.print(upos, DEC);
      Serial.print(" mpos ");
      Serial.println(mpos, DEC);
    }
  }
}

void motorCmd(int direct, int pwm) {
  if(direct == CCW) {
    digitalWrite(MOTOR_A1_PIN, LOW);
    digitalWrite(MOTOR_B1_PIN, HIGH);
  } else if(direct == CW) {
    digitalWrite(MOTOR_A1_PIN, HIGH);
    digitalWrite(MOTOR_B1_PIN, LOW);
  } else {
    digitalWrite(MOTOR_A1_PIN, LOW);
    digitalWrite(MOTOR_B1_PIN, LOW);
  }
  analogWrite(PWM_MOTOR_PIN, pwm);
}
