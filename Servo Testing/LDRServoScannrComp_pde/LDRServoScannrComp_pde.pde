import processing.serial.*;

Serial port;
float spinrad, centrex, centrey;
float[] vals;

void setup(){
  size(400, 400);
  spinrad = min(height, width)/2 - 30;
  centrex = width/2;
  centrey = height/2;
  println(Serial.list());
  port = new Serial(this, Serial.list()[2], 9600);
  rectMode(CORNERS);
  ellipseMode(RADIUS);
  vals = new float[181];
  for(int i = 0; i <= 180; i++){
    vals[i] = 0;
  }
}

int ang = 30;
void draw(){
  background(0);
  fill(50);
  strokeWeight(10);
  stroke(200, 0, 50);
  arc(centrex, centrey, spinrad, spinrad, PI, TWO_PI);
  line(centrex - spinrad, centrey, 
       centrex + spinrad, centrey);
  if(port.available() >= 3){
    if(port.read() == 'a'){
      ang = port.read();
      vals[ang] = map(port.read(),
                      0, 256,
                      0, spinrad - 10);
    }
  }
  strokeWeight(1);
  stroke(0, 255, 0);
  for(int i = 0; i <= 180; i++){
    println(millis(), i, vals[i]);
    line(centrex, centrey,
         centrex + (vals[i] * cos(-radians(i))),
         centrey + (vals[i] * sin(-radians(i))));
  }
}