import processing.serial.*;

Serial port;
float tracktop, trackbottom, centrex, centrey;
float trackx = 100;

void setup(){
  size(400, 600);
  tracktop = (height - 512)/2;
  trackbottom = height - tracktop;
  centrex = width/2;
  centrey = height/2;
  println(Serial.list());
  port = new Serial(this, Serial.list()[2], 9600);
  rectMode(CORNERS);
  ellipseMode(RADIUS);
}

int power = 0;
String words = "";
void draw(){
  background(0);
  port.write(Integer.toString(power + 255) + "P");
  noStroke();
  fill(50);
  rect(trackx + 45, tracktop - 10,
       width - 60, trackbottom + 10);
  fill(10);
  triangle((trackx + width - 15)/2, centrey,
           trackx + 45, centrey - power,
           width - 60, centrey - power);
  fill(100);
  rect(trackx + 45, centrey - power - 10, 
       width - 60, centrey - power + 10);
  fill(150);
  rect(trackx - 5, tracktop, trackx + 5, trackbottom);
  fill(255 - abs(constrain(power, -255, 0)),
       constrain(255 - abs(power * 2), 0, 255),
       255 - constrain(power, 0, 255));
  ellipse(trackx, centrey - power, 40, 10);
  fill(255);
  if(power == 0){
    words = "STATIONARY!";
  }
  else if(abs(power) < 10){
    words = "BASICALLY STOPPED!";
  }
  else{
    if(abs(power) < 100){
      words = "SLIGHT ";
    }
    else if(abs(power) < 200){
      words = "";
    }
    else{
      words = "FULL ";
    }
    if(power < 0){
      words += "REVERSE!";
    }
    else{
      words += "FORWARD!";
    }
  }
  text(words, trackx + 50, centrey - power + 5);
  text(abs(power), width - 100, centrey - power + 5);
  if(port.available() > 0){
    println(port.read());
  }
}

void mouseDragged(){
  power = -int(constrain(mouseY - centrey, -255, 255));
}

void keyPressed(){
  if(keyCode == UP){
    power = 255;
  }
  else if(keyCode == DOWN){
    power = -255;
  }
}

void keyReleased(){
  power = 0;
}

void mouseWheel(MouseEvent event){
  power = constrain(power + event.getCount(), -255, 255);
}