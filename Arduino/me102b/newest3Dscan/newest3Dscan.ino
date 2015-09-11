//#include <AccelStepper.h>
#include <StepperDriver.h>

// TURNTABLE PARAMETERS (using EasyDriver)
unsigned long turntableSteps = 200;
unsigned long turntableMicrostep = 8;
unsigned long target;
unsigned long stepsTaken;
int turntableRPM = 20;
int stepSize = 50;
int x = 0;
int revNum;
StepperDriver turntable_motor;

// SENSOR ARRAY PARAMETERS (using BigEasyDriver)
unsigned long sensorSteps = 400;
unsigned long sensorMicrostep = 16;
unsigned long changeHeight = sensorSteps*sensorMicrostep*.5;
int sensorRPM = 120;
unsigned long totalSensorSteps;
StepperDriver sensor_motor;

//IR SENSOR PARAMETERS
int bufferSize = 10;
int IR1array[10];
int IRpin1 = 0;
int sensorValue1 = 0;
int IRpin2 = 1;
int sensorValue2;
int IRpin3 = 2;
int sensorValue3;

// SYSTEM PARAMETERS
unsigned long prev;
unsigned long time;
int cmd = 0;
int done = 0;
int hidden_done = 0;
int finished = 0;

void setup()
{  
  Serial.begin(115200);
  pinMode(IRpin1, OUTPUT);
  pinMode(IRpin2, OUTPUT);
  pinMode(IRpin3, OUTPUT);
  turntable_motor.setStep(turntableSteps, 8, 9);
  turntable_motor.setSpeed(turntableMicrostep*turntableRPM);
  sensor_motor.setStep(sensorSteps, 10, 11);
  sensor_motor.setSpeed(sensorMicrostep*sensorRPM);
}

void loop()
{
  if (Serial.available())
  {
    cmd = Serial.read();
    if (cmd == '1')
    {
      x = 0;
      done = 0;
      hidden_done = 0;
      revNum = 1;
      totalSensorSteps = 0;
      while (done == 0)
      {
        scan();
        Serial.println(222222222);
        raiseSensorArray();
        int dummyArray[10];
        sensorValue3 = 0;
        for (int i = 0; i < bufferSize; i++)
        {
          dummyArray[i] = analogRead(IRpin3);
          sensorValue3 = sensorValue3 + IR1array[i];
        }
        if (sensorValue3/bufferSize < 200)
        {
          done == 1;
        }
      }
      Serial.println(999999999);
    }
    else if (cmd == '9')
    {
      resetArray();
      Serial.println(999999999);
    }
  }
}

void scan()
{
  stepsTaken = 0;
  if ((x == 0) || (x == 1))
  {
    target = 17067;
    x += 1;
  }
  else if (x == 2)
  {
    target = 17066;
    x = 0;
  }
  readIR();
  printData();
  finished = 0;
  while (finished == 0)
  {
    rotateTurntable();
    readIR();
    printData();
  }
}

void rotateTurntable()
{
  unsigned long checkStep;
  checkStep = min(stepSize,(target-stepsTaken));
  if (checkStep < stepSize)
  {
    finished = 1;
  } 
  turntable_motor.step(checkStep);
  while (turntable_motor.update() == 0)
  {
  }
  stepsTaken = stepsTaken + checkStep;
}

void raiseSensorArray()
{
  sensor_motor.step(changeHeight);
  while (sensor_motor.update() == 0)
  {
  }
  totalSensorSteps = totalSensorSteps + changeHeight;
  if (totalSensorSteps >= 576000)
  {
    hidden_done = 1;
  }
}

void resetArray()
{
  Serial.println(totalSensorSteps);
  sensor_motor.step(-1*totalSensorSteps);
  prev = millis();
  while (sensor_motor.update() == 0)
  {
    if ((millis()-prev) >= 500)
    {
      Serial.println(sensor_motor.seq_steps_left);
      prev = millis();
    }
  }
}
  
void readIR()
{
  for (int i = 0; i<bufferSize;i++)
  {
   IR1array[i] = analogRead(IRpin1);
  }
  //maxVal1 = 0;
  //minVal1 = 9999;
  //sensorValue1 = 0;
  //for (int x = 0; x < 10; x++)
  //{
   // IR1array[x] = analogRead(IRpin1);
    //sensorValue1 = sensorValue1 + IR1array[x];
    //if (IR1array[x] > maxVal1)
    //{
    //  maxVal1 = IR1array[x];
    //}
    //if (IR1array[x] < minVal1)
    //{
    //  minVal1 = IR1array[x];
    //}
}

void printData()
{
  //tpos = turntable_motor.currentPosition();
  Serial.print(stepsTaken);
  ///Serial.print(',');
  ///spos = sensor_motor.currentPosition();
  ///Serial.print(spos);
  Serial.print(',');
  for (int i = 0; i < bufferSize; i++)
  {
    Serial.print(IR1array[i]);
    Serial.print(',');
  }
  //Serial.print(sensorValue1);
  //Serial.print(',');
  //Serial.print(sensorValue2);
  //Serial.print(',');
  //Serial.print(sensorValue3);
  Serial.println();
}
