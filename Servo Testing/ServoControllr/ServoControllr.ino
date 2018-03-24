#include <Servo.h>

Servo servo;

void setup() {
  servo.attach(10);
  servo.write(0);
  delay(2000);
  Serial.begin(9600);
}

void loop() {
  if(Serial){
    if(Serial.available()){
      int ang = constrain(Serial.parseInt(), 0, 180);
      Serial.println(ang);
      servo.write(ang);
    }
  }
}
