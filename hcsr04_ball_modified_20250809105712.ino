#include <NewPing.h>
#define trig1 2
#define echo1 3
#define trig2 4
#define echo2 5
#define trig3 6
#define echo3 7
#define max_distance 100
int d1;
int d2;
int d3;

const int wall1=40;
const int wall2=40;
const int wall3=30;

NewPing sonar1(trig1,echo1,max_distance);
NewPing sonar2(trig2,echo2,max_distance);
NewPing sonar3(trig3,echo3,max_distance);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  d1=sonar1.ping_cm(50);
  d2=sonar2.ping_cm(50);
  d3=sonar3.ping_cm(50);
  
  if(d1==0) d1=wall1;
  if(d2==0) d2=wall2;
  if(d3==0) d3=wall3;

Serial.print("d1 is:"); 
Serial.print(d1);
Serial.print(", d2 is:");
Serial.print(d2);
Serial.print(", d3 is:");
Serial.println(d3);

  delay(100);
}