//#include <AccelStepper.h>
#include <StepperDriver.h>

// TURNTABLE PARAMETERS (using EasyDriver)
unsigned long turntableSteps = 200;
unsigned long turntableMicrostep = 8;
unsigned long target;
unsigned long stepsTaken;
int turntableRPM = 20;
int stepSize = 100;
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
int array1[10];
int sensorValue1;
int ir_1;
int minVal1;
int maxVal1;
int sensorValue2;
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
  Serial.begin(9600);
  turntable_motor.setStep(turntableSteps, 8, 9);
  turntable_motor.setSpeed(turntableMicrostep*turntableRPM);
  sensor_motor.setStep(sensorSteps, 10, 11);
  sensor_motor.setSpeed(sensorMicrostep*sensorRPM);
  totalSensorSteps = 0;
  x = 0;
}

void loop()
{
  if (Serial.available())
  {
    cmd = Serial.read();
    if (cmd == '1')
    {
      scan();
      Serial.println(222222222);
    }
    else if (cmd == '2')
    {
      raiseSensorArray();
      readIR();
      if (ir_1 < 200)
      {
        Serial.println(999999999);
      }
      else
      {
        Serial.println(444444444);
      }
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
  int i = 0;
  sensorValue1 = 0;
  maxVal1 = 0;
  minVal1 = 9999;
  delay(25);
  for (i = 0; i < bufferSize; i++)
  {
    array1[i] = analogRead(A0);
    sensorValue1 = sensorValue1 + array1[i];
    delay(10);
    if (minVal1 > array1[i])
    {
      minVal1 = array1[i];
    }
    if (maxVal1 < array1[i])
    {
      maxVal1 = array1[i];
    }
  }
  ir_1 = (sensorValue1-minVal1-maxVal1)/(bufferSize-2);
}

void printData()
{
  Serial.print(stepsTaken);
  Serial.print(',');
  Serial.print(ir_1);
  //Serial.print(sensorValue1);
  //Serial.print(',');
  //Serial.print(sensorValue2);
  //Serial.print(',');
  //Serial.print(sensorValue3);
  Serial.println();
}
