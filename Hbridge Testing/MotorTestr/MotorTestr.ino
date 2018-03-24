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
}

int i = 1;
int inc = 5;
int pulsewidth = 0;

void loop(){
  pulsewidth = int(255 * sin(radians(i/10)));
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
  i++;
  if(i % 10 == 0){
    pulsewidth += inc;
    if(abs(pulsewidth) == 255){
      inc *= -1;
    }
  }
}

