#include <Servo.h>

Servo servo;
int servopin = 10;
int LDRpin = 0;
int calibrationpin = 1;

void setup() {
  servo.attach(10);
  servo.write(90);
  delay(2000);
  Serial.begin(9600);
}

float ang = 90;
void loop() {
  if(Serial){
    Serial.println(ang);
  }
  int LDRvoltage = analogRead(LDRpin);
  int calibrationvoltage = analogRead(calibrationpin);
  ang += (calibrationvoltage - LDRvoltage)/100;
  ang = constrain(ang, 0, 180);
  servo.write(ang);
}
