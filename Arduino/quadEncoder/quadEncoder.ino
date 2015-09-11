/* Encoder Library - TwoKnobs Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>

// Change these pin numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability

Encoder quad(5, 6);
long qPos;
//   avoid using pins with LEDs attached

void setup() {
  Serial.begin(9600);
  Serial.println("TwoKnobs Encoder Test:");
}

//long positionLeft  = -999;
//long positionRight = -999;

void loop() {
  qPos = quad.read();
  Serial.println(qPos);
  delay(10);
//  long newLeft;
//  newLeft = knobLeft.read();
//  newRight = knobRight.read();
//  if (newLeft != positionLeft || newRight != positionRight) {
//    Serial.print("Left = ");
//    Serial.print(newLeft);
//    Serial.print(", Right = ");
//    Serial.print(newRight);
//    Serial.println();
//    positionLeft = newLeft;
//    positionRight = newRight;
//  }
}
