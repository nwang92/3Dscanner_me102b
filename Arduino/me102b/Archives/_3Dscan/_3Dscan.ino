#include <AccelStepper.h>
#include <StepperDriver.h>

// TURNTABLE PARAMETERS (using EasyDriver)
const double turntableSteps = 200;
const double turntableMicrostep = 8; // CHANGE TO 8 IF USING EASYDRIVER
double turntableRPM = 32; // set motor RPM
float turntableSpeed = turntableSteps*turntableMicrostep/60.0*turntableRPM;
double stageRevolutionSteps = turntableSteps*turntableMicrostep*32/3.0;
unsigned long tpos;
int motor1DirPin = 8; //digital pin 2
int motor1StepPin = 9; //digital pin 3
AccelStepper turntable_motor(1, motor1StepPin, motor1DirPin); 

// IR SENSOR ARRAY PARAMETERS (using BigEasyDriver)
const double sensorSteps = 400;
const double sensorMicrostep = 16; // CHANGE TO 8 IF USING EASYDRIVER
double sensorRPM = 120; // set motor RPM
float sensorSpeed = sensorSteps*sensorMicrostep/60.0*sensorRPM;
unsigned long spos;
int motor2DirPin = 10; //digital pin 4
int motor2StepPin = 11; //digital pin 5
AccelStepper sensor_motor(1, motor2StepPin, motor2DirPin); 

//IR SENSOR PARAMETERS
int IRpin1 = 0;
int sensorValue1;
int IRpin2 = 1;
int sensorValue2;
int IRpin3 = 2;
int sensorValue3 = 5;
int MAXIRSENSORLIMIT = 150;

// SYSTEM PARAMETERS
int total_scan_time = 25*1000;
unsigned long prev;
unsigned long time;
int time_between_data = .5*1000;
int cmd = 0;
int done = 0;

void setup()
{  
  Serial.begin(115200);
  pinMode(IRpin1, OUTPUT);
  pinMode(IRpin2, OUTPUT);
  pinMode(IRpin3, OUTPUT);
  turntable_motor.setCurrentPosition(0);
  sensor_motor.setCurrentPosition(0);
  turntable_motor.setMaxSpeed(turntableSpeed);
  sensor_motor.setMaxSpeed(sensorSpeed);
  turntable_motor.setSpeed(turntableSpeed);
  sensor_motor.setSpeed(sensorSpeed);
  done = 0;
}
void loop()
{  
  if (Serial.available())
  {
    cmd = Serial.read();
    if (cmd == '1' || cmd == '15' || cmd == '30' || cmd == '40')
    {
      prev = millis();
      while (done == 0)
      {
        rotateTurntable();
        raiseSensorArray();
        readIR();
        printData();
      }
      stopMotors();
      Serial.print('DONE');
      sensor_motor.setSpeed(-1*sensorSpeed);
      while (done == 1)
      {
        resetSensorPosition();
        time = millis();
        if (((time-prev)%time_between_data) == 0)
        {
          spos = sensor_motor.currentPosition();
          Serial.println(spos);
        }
      }
      turntable_motor.stop();
      sensor_motor.stop();
      Serial.println(999999999);
    }
  }
}

void rotateTurntable()
{ 
  time = millis();
  if (time-prev >= total_scan_time)
  {
    stopMotors();
    done = 1;
  }
  runMotors();
}

void raiseSensorArray()
{
  //276480000
  if ((sensor_motor.currentPosition() >= 10000)) //(sensorValue3 <= 150) 
  {
    sensor_motor.setSpeed(-1*sensorSpeed);
    sensor_motor.runSpeed();
  }
  else if (sensor_motor.currentPosition() <= 0)
  {
    sensor_motor.setSpeed(sensorSpeed);
    sensor_motor.runSpeed();
  }
  runMotors();
}
  
void readIR()
{
  runMotors();
  sensorValue1 = analogRead(IRpin1);
  sensorValue2 = analogRead(IRpin2);
  sensorValue3 = analogRead(IRpin3);
  runMotors();
}

void resetSensorPosition()
{
  if (sensor_motor.currentPosition() <= 0)
  {
    sensor_motor.stop();
    done = 2;
  }
  turntable_motor.stop();
  sensor_motor.runSpeed();
}

void runMotors()
{
  turntable_motor.runSpeed();
  sensor_motor.runSpeed();
}

void stopMotors()
{
  turntable_motor.stop();
  sensor_motor.stop();
}

void printData()
{
  time = millis();
  if (((time-prev)%time_between_data) == 0)
  {
    tpos = turntable_motor.currentPosition();
    Serial.print(tpos);
    Serial.print(',');
    spos = sensor_motor.currentPosition();
    Serial.print(spos);
    Serial.print(',');
    Serial.print(sensorValue1);
    Serial.print(',');
    Serial.print(sensorValue2);
    Serial.print(',');
    Serial.print(sensorValue3);
    Serial.println();
  }
}
