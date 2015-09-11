int cmd;
int irpin1 = 0;
int irpin2 = 1;
int irpin3 = 2;
int senVal1;
int senVal2;
int senVal3;

int bufferSize = 15;
int buffer[15];
int i;

void setup() {
    Serial.begin(115200);
    pinMode(irpin1,OUTPUT);
    pinMode(irpin2,OUTPUT);
    pinMode(irpin3,OUTPUT);
}
void loop() 
{
  senVal1 = 0;
  for (i = 0; i < bufferSize; i++)
  {
    buffer[i] = analogRead(irpin1);
    senVal1 = senVal1 + buffer[i];
  }
  //Serial.println(senVal1/bufferSize);
  Serial.println(senVal1/1023.0/bufferSize*500);
  delay(100);
}
