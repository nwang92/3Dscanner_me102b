//#include <AccelStepper.h>
#include <StepperDriver.h>

// TURNTABLE PARAMETERS (using EasyDriver)
unsigned long turntableSteps = 200;
unsigned long turntableMicrostep = 8;
unsigned long target;
unsigned long stepsTaken;
int turntableRPM = 32;
int stepSize = 100;
int x = 0;
int revNum;
StepperDriver turntable_motor;

// SENSOR ARRAY PARAMETERS (using BigEasyDriver)
unsigned long sensorSteps = 400;
unsigned long sensorMicrostep = 16;
unsigned long changeHeight = sensorSteps*sensorMicrostep*2;
int sensorRPM = 120;
unsigned long totalSensorSteps;
StepperDriver sensor_motor;

//IR SENSOR PARAMETERS
int bufferSize = 10;
int maxVal1 = 0;
int minVal1 = 9999;
int IR1array[10];
int IRpin1 = 0;
int sensorValue1 = 0;
int IRpin2 = 1;
int sensorValue2;
int IRpin3 = 2;
int sensorValue3;

// SYSTEM PARAMETERS
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
  x = 0;
}
void loop()
{
  if (Serial.available())
  {
    cmd = Serial.read();
    if ((cmd == '1') || (cmd == '2') || (cmd == '3'))
    {
      done = 0;
      hidden_done = 0;
      revNum = 1;
      totalSensorSteps = 0;
      while (done == 0)
      {
        scan();
        Serial.println(222222222);
        raiseSensorArray();
        ////revNum = revNum+1;
        //if (revNum > 1)
        //{
        //  done = 1;
        //}
        readIR();
        if ((sensorValue1-minVal1-maxVal1)/(bufferSize-2) < 100)
        {
          done = 1;
        }
        if (hidden_done == 1)
        {
          scan();
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
  int didItStop;
  int interruptStep;
  didItStop = 0;
  sensor_motor.step(changeHeight);
  while (sensor_motor.update() == 0)
  {
  }
  if (didItStop == 0)
  {
    totalSensorSteps = totalSensorSteps + changeHeight;
    if (totalSensorSteps >= 576000)
    {
      hidden_done = 1;
    }
  }
  else if (didItStop == 1)
  {
    sensor_motor.step(-10);
    while (sensor_motor.update() == 0)
    {
    }
    totalSensorSteps = totalSensorSteps + changeHeight - interruptStep - 10;
    hidden_done = 1;
  }
}

void resetArray()
{
  sensor_motor.step(-1*totalSensorSteps);
  while (sensor_motor.update() == 0)
  {
  }
}
  
void readIR()
{
  delay(10);
  maxVal1 = 0;
  minVal1 = 9999;
  sensorValue1 = 0;
  for (int i = 0; i<bufferSize;i++){
   IR1array[i] = analogRead(IRpin1);
   sensorValue1 = sensorValue1 + IR1array[i];
   if (IR1array[i] > maxVal1)
   {
     maxVal1 = IR1array[i];
   }
   if (IR1array[i] < minVal1)
   {
     minVal1 = IR1array[i];
   }
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
  Serial.print((sensorValue1-minVal1-maxVal1)/(bufferSize-2));
  //Serial.print(sensorValue1);
  //Serial.print(',');
  //Serial.print(sensorValue2);
  //Serial.print(',');
  //Serial.print(sensorValue3);
  Serial.println();
}
