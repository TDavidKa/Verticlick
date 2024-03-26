#include <Adafruit_CircuitPlayground.h>
float X, Y, Z;
bool L, R;
int id = 0;

void setup() {
  Serial.begin(9600);
  CircuitPlayground.begin();
}

void loop() {
  id += 1;
  X = CircuitPlayground.motionX();
  Y = CircuitPlayground.motionY();
  Z = CircuitPlayground.motionZ();
  L = CircuitPlayground.leftButton();
  R = CircuitPlayground.rightButton();


  Serial.print("{" + String(id) + "," + String(X) + "," + String(Y) + "," + String(Z) + "," + String(L) + "," + String(R) + "}");


  delay(10);
}