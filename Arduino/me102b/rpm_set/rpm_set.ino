#include <StepperDriver.h>

const int stepsPerRevolution = 400; // change this to fit the number of steps per revolution for your motor
const int microstep = 16;
int rpm = 2*60; // set motor RPM
int dir = 1;
int x;
unsigned long time;
unsigned long prev;
StepperDriver myStepper; //initialize for one stepper

void setup() {
  Serial.begin(9600);
  myStepper.setStep(stepsPerRevolution, 10, 11);
  myStepper.setSpeed(rpm*microstep); //with 1/8th stepping turned on, 1 rpm * 8 = 8
  myStepper.step(dir*stepsPerRevolution*microstep); //with 1/8 stepping turned on, one full revolution needs to be multiplied x 8
  x = 0;
}

void loop() {
  //Serial.println(myStepper.seq_steps_left);
  if (myStepper.update() == 1)
  { 
    if (x < 20)
    {
      x = x+1;
      myStepper.step(dir*stepsPerRevolution*microstep*.5);
      delay(1000);
    }
    else
    {
      myStepper.step(0);
    }
  }
}
