#include <Servo.h>

Servo Lservo;
Servo Rservo;

void setup(){
  Lservo.attach(10);
  Lservo.write(0);
  Rservo.attach(8);
  Rservo.write(0);
  delay(2000);
  Serial.begin(9600);
}

void loop() {
  if(Serial){
    if(Serial.available()){
      char which = Serial.read();
      Serial.write(which);
      if(which == 'L'){
        int Lang = constrain(Serial.parseInt(), 0, 180);
        Serial.println("LEFT:");
        Serial.println(Lang);
        Lservo.write(Lang);
      }
      else if(which == 'R'){
        int Rang = constrain(Serial.parseInt(), 0, 180);
        Serial.println("RIGHT:");
        Serial.println(Rang);
        Rservo.write(Rang);
      }
    }
  }
}
