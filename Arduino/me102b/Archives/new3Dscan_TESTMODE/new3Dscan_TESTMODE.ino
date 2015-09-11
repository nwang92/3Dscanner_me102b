#include <AccelStepper.h>
#include <StepperDriver.h>

// TURNTABLE PARAMETERS (using EasyDriver)
const double turntableSteps = 200;
const double turntableMicrostep = 8; // CHANGE TO 8 IF USING EASYDRIVER
double turntableRPM = 32; // set motor RPM
float turntableSpeed = turntableSteps*turntableMicrostep/60.0*turntableRPM;
double stageRevolutionSteps = turntableSteps*turntableMicrostep*32/3.0;
unsigned long tpos;
int revNum;
int motor1DirPin = 8; //digital pin 2
int motor1StepPin = 9; //digital pin 3
AccelStepper turntable_motor(1, motor1StepPin, motor1DirPin); 

// IR SENSOR ARRAY PARAMETERS (using BigEasyDriver)
unsigned long sensorSteps = 400;
unsigned long sensorMicrostep = 16; // CHANGE TO 8 IF USING EASYDRIVER
unsigned long changeHeight = sensorSteps*sensorMicrostep*2;
int sensorRPM = 120;
unsigned long totalSensorSteps = 0;
int motor2DirPin = 10;
int motor2StepPin = 11;
StepperDriver sensor_motor;
//float sensorSpeed = sensorSteps*sensorMicrostep/60.0*sensorRPM;
//AccelStepper sensor_motor(1, motor2StepPin, motor2DirPin); 

//IR SENSOR PARAMETERS
int bufferSize = 5;
int IR1array[5];
int index1 = 0;
int IRpin1 = 0;
int sensorValue1 = 0;
int IRpin2 = 1;
int sensorValue2;
int IRpin3 = 2;
int sensorValue3;
int MAXIRSENSORLIMIT = 150;

// SYSTEM PARAMETERS
unsigned long prev;
unsigned long time;
unsigned long testprev;
unsigned long testtime;
int time_between_data = .25*1000;
int cmd = 0;
int done = 0;
int hidden_done = 0;
int finished = 0;
int reading = 0;

void setup()
{  
  Serial.begin(115200);
  pinMode(IRpin1, OUTPUT);
  pinMode(IRpin2, OUTPUT);
  pinMode(IRpin3, OUTPUT);
  turntable_motor.setCurrentPosition(0);
  turntable_motor.setMaxSpeed(turntableSpeed);
  turntable_motor.setSpeed(turntableSpeed);
  sensor_motor.setStep(sensorSteps, motor2DirPin, motor2StepPin);
  sensor_motor.setSpeed(sensorMicrostep*sensorRPM);
}
void loop()
{
  if (Serial.available())
  {
    cmd = Serial.read();
    if ((cmd == '1') || (cmd == '2') || (cmd == '3'))
    {
      delay(1);
      revNum = 1;
      done = 0;
      hidden_done = 0;
      while (done == 0)
      {
        finished = 0;
        prev = millis();
        index1 = 0;
        while (finished == 0)
        {
          printData();
          turntable_motor.runSpeed();
          readIR();
          rotateTurntable();
        }
        turntable_motor.stop();
        //raiseSensorArray();
        revNum = revNum+1;
        if (revNum > 1)
        {
          done = 1;
        }
        //checkHiddenDone()
      }
      turntable_motor.stop();
      //resetArray();
      Serial.println(99999999);
    }
  }
}

void rotateTurntable()
{
  if (turntable_motor.currentPosition() >= revNum*stageRevolutionSteps) //(turntable_motor.currentPosition() >= stageRevolutionSteps)
  {
    turntable_motor.stop();
    finished = 1;
  }
  else
  {
    turntable_motor.runSpeed();
  }
}

void raiseSensorArray()
{
  totalSensorSteps = totalSensorSteps + changeHeight;
  if (totalSensorSteps > 672000)
  {
    sensor_motor.step(672000-totalSensorSteps);
    hidden_done = 1;
  } 
  else
  {
    sensor_motor.step(changeHeight);
  }
  while (sensor_motor.update() == 0)
  {
    if (totalSensorSteps-sensor_motor.seq_steps_left >= 64000) //||(sensorValue1 < 125)
    {
      totalSensorSteps = totalSensorSteps - sensor_motor.seq_steps_left;
      hidden_done = 1;
      sensor_motor.step(0);
    }
  }
}

void resetArray()
{
  sensor_motor.step(-1*totalSensorSteps);
  while (sensor_motor.update() == 0)
  {
  }
}

void checkHiddenDone()
{
  if (hidden_done == 1)
  {
    finished = 0;
    prev = millis();
    index1 = 0;
    while (finished == 0)
    {
      printData();
      turntable_motor.runSpeed();
      readIR();
      rotateTurntable();
    }
    turntable_motor.stop();
    done = 1;
  }
}
  
void readIR()
{
  sensorValue1 = analogRead(IRpin1);
  //sensorValue2 = analogRead(IRpin2);
  //sensorValue3 = analogRead(IRpin3);
}

void printData()
{
  //turntable_motor.runSpeed();
  time = millis();
  if ((time-prev) >= time_between_data)
  {
    //tpos = turntable_motor.currentPosition();
    Serial.print(turntable_motor.currentPosition());
    ///Serial.print(',');
    ///spos = sensor_motor.currentPosition();
    ///Serial.print(spos);
    Serial.print(',');
    Serial.print(sensorValue1);
    //Serial.print(',');
    //Serial.print(sensorValue2);
    //Serial.print(',');
    //Serial.print(sensorValue3);
    Serial.println();
    prev = millis();
  }
}
