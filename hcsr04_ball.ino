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
NewPing sonar1(trig1,echo1,max_distance);
NewPing sonar2(trig2,echo2,max_distance);
NewPing sonar3(trig3,echo3,max_distance);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  d1=sonar1.ping_cm();
  d2=sonar2.ping_cm();
  d3=sonar3.ping_cm();
  

  Serial.print(d1,",");
  Serial.print(d2,",");
  Serial.print(d3);
  Serial.print("\n");


  

  delay(100);
}