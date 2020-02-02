
/*
  Stepper Motor Control - one revolution
  RPM = 60*(number of steps/second)/(number of steps/revolution)
  Steps per Revolution = 360 / 1.8 = 200
  RPM = 60 * 800 / 200
*/

#include <Stepper.h>

const int STEPS = 200;
unsigned long previousMillis = 0;
unsigned long currentMillis;

Stepper myStepper(STEPS, 11, 12);

void setup() {
  Serial.begin(115200);
  myStepper.setSpeed(3000);
}

void loop() {
  while (Serial.available() > 0) {
    String incoming = Serial.readStringUntil('\n');
    int position = incoming.toInt();
    myStepper.step(position);
  }
}
