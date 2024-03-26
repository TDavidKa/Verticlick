#include <Adafruit_CircuitPlayground.h>
float X, Y, Z;
bool L, R;

void setup() {
  Serial.begin(9600);
  CircuitPlayground.begin();
}

void loop() {
  X = CircuitPlayground.motionX();
  Y = CircuitPlayground.motionY();
  L = CircuitPlayground.leftButton();
  R = CircuitPlayground.rightButton();

  


  Serial.print("{" + String(X) + "," + String(Y) + "," + String(L) + "," + String(R) + "}");


  delay(10);
}