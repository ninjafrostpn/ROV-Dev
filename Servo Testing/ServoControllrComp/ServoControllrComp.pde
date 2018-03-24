import processing.serial.*;

Serial port;
float spinrad, centrex, centrey;

void setup(){
  size(400, 400);
  spinrad = min(height, width)/2 - 30;
  centrex = width/2;
  centrey = height/2;
  println(Serial.list());
  port = new Serial(this, Serial.list()[2], 9600);
  port.write(Integer.toString(0) + "A");
  rectMode(CORNERS);
  ellipseMode(RADIUS);
}

int ang = 30;
void draw(){
  background(0);
  //println(ang);
  port.write(Integer.toString(ang) + "A");
  stroke(200, 0, 50);
  strokeWeight(10);
  fill(50);
  arc(centrex, centrey, spinrad, spinrad, PI, TWO_PI);
  line(centrex - spinrad, centrey, 
       centrex + spinrad, centrey);
  line(centrex, centrey,
       centrex + ((spinrad - 20) * cos(-radians(ang))),
       centrey + ((spinrad - 20) * sin(-radians(ang))));
  ellipse(centrex, centrey, 10, 10);
  fill(255);
  textSize(70);
  text(str(ang), 
       centrex + ((spinrad - 40) * cos(-radians(ang))) - 5,
       centrey + ((spinrad - 40) * sin(-radians(ang))) + 5);
  if(port.available() > 0){
    println(port.read());
  }
}

void mouseDragged(){
  if(mouseY < centrey){
    ang = constrain(int(degrees(-atan2(mouseY - centrey, mouseX - centrex))), 0, 180);
  }
}

void keyPressed(){
  if(keyCode == LEFT){
    ang = constrain(ang + 10, 0, 180);
  }
  else if(keyCode == RIGHT){
    ang = constrain(ang - 10, 0, 180);
  }
}