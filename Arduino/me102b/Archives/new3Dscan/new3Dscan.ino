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
int sensorRPM = 120;
int dir = 1;
unsigned long totalSensorSteps = 0;
int motor2DirPin = 10;
int motor2StepPin = 11;
StepperDriver sensor_motor;
//float sensorSpeed = sensorSteps*sensorMicrostep/60.0*sensorRPM;
//AccelStepper sensor_motor(1, motor2StepPin, motor2DirPin); 

//IR SENSOR PARAMETERS
int IRpin1 = 0;
int sensorValue1;
int IRpin2 = 1;
int sensorValue2;
int IRpin3 = 2;
int sensorValue3;
int MAXIRSENSORLIMIT = 150;

// SYSTEM PARAMETERS
unsigned long prev;
unsigned long time;
int time_between_data = .25*1000;
int cmd = 0;
int done = 0;
int first = 0;
int doneRising = 0;
int finished = 0;

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
  done = 0;
  finished = 0;
}
void loop()
{  
  if (Serial.available())
  {
    cmd = Serial.read();
    if (cmd == '1' || cmd == '15' || cmd == '30' || cmd == '40')
    {
      revNum = 1;
      while (finished == 0)
      {
        done = 0;
        prev = millis();
        while (done == 0)
        {
          rotateTurntable();
          readIR();
          printData();
        }
        turntable_motor.stop();
        doneRising = 0;
        totalSensorSteps = totalSensorSteps + sensorSteps*sensorMicrostep*1.5;
        sensor_motor.step(sensorSteps*sensorMicrostep*1.5);
        totalSensorSteps = totalSensorSteps + sensorSteps*sensorMicrostep*1.5;
        while (sensor_motor.update() == 0);
        {
          Serial.println(22222);
          raiseSensorArray();
        }
        revNum = revNum+1;
      }
      Serial.println(999999999);
    }
  }
}

void rotateTurntable()
{
  if (turntable_motor.currentPosition() >= revNum*stageRevolutionSteps) //(turntable_motor.currentPosition() >= stageRevolutionSteps)
  {
    turntable_motor.stop();
    done = 1;
    Serial.println('DONE');
  }
  else
  {
    turntable_motor.runSpeed();
  }
}

void raiseSensorArray()
{
  //276480000
}
  
void readIR()
{
  turntable_motor.runSpeed();
  sensorValue1 = analogRead(IRpin1);
  sensorValue2 = analogRead(IRpin2);
  sensorValue3 = analogRead(IRpin3);
}

void resetSensorPosition()
{
}

void printData()
{
  turntable_motor.runSpeed();
  time = millis();
  if (((time-prev)%time_between_data) == 0)
  {
    tpos = turntable_motor.currentPosition();
    Serial.print(tpos);
    ///Serial.print(',');
    ///spos = sensor_motor.currentPosition();
    ///Serial.print(spos);
    Serial.print(',');
    Serial.print(sensorValue1);
    Serial.print(',');
    Serial.print(sensorValue2);
    Serial.print(',');
    Serial.print(sensorValue3);
    Serial.println();
  }
}
