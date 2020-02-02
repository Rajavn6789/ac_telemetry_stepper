
#include <AccelStepper.h>
AccelStepper stepper(AccelStepper::DRIVER, 12, 11);

const int MAX_SPEED = 3000;
const long interval = 30;
unsigned long previousMillis = 0;

void setup()
{
  stepper.setMaxSpeed(MAX_SPEED);
  Serial.begin(115200);
  delay(2000);
  Serial.setTimeout(10);
}
void loop()
{
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval && Serial.available() > 0) {
    String incoming = Serial.readStringUntil('\n');
    int position = incoming.toInt();
    if (abs(position) < 4000) {
      stepper.moveTo(position);
      stepper.setSpeed(MAX_SPEED);
    }
    previousMillis = currentMillis;
  }
  stepper.runSpeedToPosition();
}
