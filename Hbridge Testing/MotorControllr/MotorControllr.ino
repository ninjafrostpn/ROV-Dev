int LeftsPin = 11;
int RightsPin = 12;
int PWMPin = 10; //BEWARE: PWM function works on pins 3, 5, 6, 9, 10, and 11... not 13

void setup(){
  pinMode(LeftsPin, OUTPUT);
  digitalWrite(LeftsPin, LOW);
  pinMode(RightsPin, OUTPUT);
  digitalWrite(RightsPin, LOW);
  pinMode(PWMPin, OUTPUT);
  digitalWrite(PWMPin, LOW);
  Serial.begin(9600);
}

int pulsewidth = 0;

void loop(){
  if(Serial){
    if(Serial.available()){
      int pulsewidth = Serial.parseInt() - 255;
      Serial.println(pulsewidth);
      if(pulsewidth < 0){
        pulsewidth = -pulsewidth;
        digitalWrite(LeftsPin, LOW);
        digitalWrite(RightsPin, HIGH);
      }
      else if(pulsewidth > 0){
        digitalWrite(LeftsPin, HIGH);
        digitalWrite(RightsPin, LOW);
      }
      else{
        digitalWrite(LeftsPin, LOW);
        digitalWrite(RightsPin, LOW);
      }
      analogWrite(PWMPin, constrain(pulsewidth, 0, 255));
    }
  }
}

