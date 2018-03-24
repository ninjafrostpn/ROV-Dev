import processing.serial.*;

Serial port;
float spinrad, centrex, centrey;

class Dial{
  char ID;
  float posx, posy;
  int ang;
  Dial(char IDin, float posxin, float posyin, int angin){
    ID = IDin;
    posx = posxin;
    posy = posyin;
    ang = angin;
    port.write(str(ID) + Integer.toString(0) + "A");
  }
  
  void show(int angin){
    ang = constrain(ang + angin, 0, 180);
    //println(ang);
    port.write(str(ID) + Integer.toString(ang) + "A");
    stroke(200, 0, 50);
    strokeWeight(10);
    fill(50);
    arc(posx, posy, spinrad, spinrad, PI, TWO_PI);
    line(posx - spinrad, posy, 
         posx + spinrad, posy);
    line(posx, posy,
         posx + ((spinrad - 20) * cos(-radians(ang))),
         posy + ((spinrad - 20) * sin(-radians(ang))));
    ellipse(posx, posy, 10, 10);
    fill(255);
    textSize(70);
    text(str(ang), 
         posx + ((spinrad - 40) * cos(-radians(ang))) - 5,
         posy + ((spinrad - 40) * sin(-radians(ang))) + 5);
  }
  
  void inc(int angin){
    ang = constrain(ang + angin, 0, 180);
  }
  
  void toMouse(){
    ang = constrain(int(degrees(-atan2(mouseY - posy, mouseX - posx))), 0, 180);
  }
}

Dial Ldial, Rdial;

void setup(){
  size(800, 400);
  spinrad = min(height, width/2)/2 - 30;
  centrex = width/2;
  centrey = height/2;
  println(Serial.list());
  port = new Serial(this, Serial.list()[2], 9600);
  Ldial = new Dial('L', centrex/2, centrey, 90);
  Rdial = new Dial('R', centrex * 1.5, centrey, 90);
  rectMode(CORNERS);
  ellipseMode(RADIUS);
}

int Linc = 0;
int Rinc = 0;
void draw(){
  background(0);
  Ldial.show(Linc);
  Rdial.show(Rinc);
  if(port.available() > 0){
    println(port.read());
  }
}

int side = 0;
void mouseDragged(){
  if(mouseY < centrey){
    if((mouseX < centrex && side < 1) || side == -1){
      Ldial.toMouse();
      side = -1;
    }
    else if((mouseX > centrex && side > -1) || side == 1){
      Rdial.toMouse();
      side = 1;
    }
  }
}

void mouseReleased(){
  side = 0;
}

void keyPressed(){
  if(key == 'a'){
    Linc += 1;
  }
  else if(key == 'd'){
    Linc -= 1;
  }
  else if(keyCode == LEFT){
    Rinc += 1;
  }
  else if(keyCode == RIGHT){
    Rinc -= 1;
  }
  Rinc = constrain(Rinc, -1, 1);
  Linc = constrain(Linc, -1, 1);
}

void keyReleased(){
  if(key == 'a'){
    Linc = 0;
  }
  else if(key == 'd'){
    Linc = 0;
  }
  else if(keyCode == LEFT){
    Rinc = 0;
  }
  else if(keyCode == RIGHT){
    Rinc = 0;
  }
}