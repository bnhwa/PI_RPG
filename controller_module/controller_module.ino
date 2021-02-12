/**********************************************************************
sends bytes over to python, each byte position indicates somtheing
much more efficient than sending strings!
**********************************************************************/
int xyzPins[] = {13, 12, 14};   //x,y,z pins
#define pin_button1 18
#define pin_button2 19
#define pin_button3 15
void setup() {
  Serial.begin(9600);//115200
  pinMode(pin_button1,INPUT);
  pinMode(pin_button2,INPUT);
  pinMode(pin_button3,INPUT);
  pinMode(xyzPins[2], INPUT_PULLUP);  //z axis is a button.
}

void loop() {
  //send byte over to python
  
//  byte x = 0b10000000;// 10000000
  
  int xVal = analogRead(xyzPins[0]);//x from top0 --- 4096bottom
  int yVal = analogRead(xyzPins[1]);//y from top0 ---4096bottom
  int zVal = digitalRead(xyzPins[2]);
  byte send_out = set_direc(xVal,yVal);
  byte b1 = 1;
  if(digitalRead(pin_button1)==LOW){
    b1 = 1;
  }else{
    b1 = 0;
  }
  byte b2 = 1;
  if(digitalRead(pin_button2)==LOW){
    b2 = 1;
  }else{
    b2 = 0;
  }
  byte b3 = 1;
  if(digitalRead(pin_button3)==LOW){
    b3 = 1;
  }else{
    b3 = 0;
  }
  bitWrite(send_out, 4, b1);
  bitWrite(send_out, 5, b2);
  bitWrite(send_out,6,b3);
  Serial.println(send_out);
//  Serial.println(send_out);
//  Serial.println(moving(yVal));
  //Serial.printf("X,Y,Z: %d,\t%d,\t%d\n", xVal, yVal, zVal);
  delay(500);
}


byte set_direc(int xVal, int yVal){
   byte x = 0b10000000;// 10000000
//  bitWrite(x, 0, 1);
  //left/right/nomoving
   bitWrite(x, 0, lr(xVal));
   bitWrite(x, 1, moving(xVal));
   //up/down/idle
   bitWrite(x, 2, lr(yVal));
   bitWrite(x, 3, moving(yVal));
  return x;
}
byte lr(int pos){
  if ((pos-2048)>0){
    return 1;
  }else{
    return 0;
  }
}
byte moving(int pos){
  int ok = abs(pos-2048);
  if (ok >700){
    return 1;
  }else{
    return 0;
  }
}
