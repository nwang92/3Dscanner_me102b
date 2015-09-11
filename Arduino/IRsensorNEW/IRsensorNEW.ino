/*
  ReadAnalogVoltage
  Reads an analog input on pin 0, converts it to voltage, and prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */
int array1[10];
int bufferSize = 10;
int sensorValue1;
int minVal1;
int maxVal1;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop()
{
  int i = 0;
  sensorValue1 = 0;
  maxVal1 = 0;
  minVal1 = 9999;
  for (i = 0; i < bufferSize; i++)
  {
    array1[i] = analogRead(A0);
    sensorValue1 = sensorValue1 + array1[i];
    if (minVal1 > array1[i])
    {
      minVal1 = array1[i];
    }
    if (maxVal1 < array1[i])
    {
      maxVal1 = array1[i];
    }
  }
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  // print out the value you read:
  //Serial.print(sensorValue1/10);
  //Serial.print(',');
  //Serial.print(maxVal1);
  //Serial.print(',');
  //Serial.print(minVal1);
  Serial.print((sensorValue1-minVal1-maxVal1)/10);
//  Serial.print((sensorValue2-minVal2-maxVal2)/8);
//  Serial.print(',');
//  Serial.print((sensorValue3-minVal3-maxVal3)/8);
  Serial.println();
}
