#include <Servo.h>

Servo servo;
int servopin = 10;
int LDRpin = 0;

void setup() {
  servo.attach(10);
  servo.write(90);
  delay(1000);
  delay(2000);
  Serial.begin(9600);
}

int ang = 90;
int inc = 1;
void loop() {
  servo.write(ang);
  int LDRvoltage = analogRead(LDRpin);
  if(Serial){
    Serial.write('a');
    Serial.write(ang);
    Serial.write(LDRvoltage);
  }
  if(constrain(ang, 1, 179) != ang){
    inc *= -1;
  }
  ang += inc;
  delay(20);
}
