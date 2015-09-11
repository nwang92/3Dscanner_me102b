const int CC = 4;
const int BB = 5;
const int G = 6;
const int F = 7;
const int A = 8;
const int B = 9;
const int E = 10;
const int D = 11;
const int C = 12;
const int dp = 13;
 
void setup() {
 
pinMode(CC,4);
pinMode(BB,5);
pinMode(G,6);
pinMode(F,7);
pinMode(A,8);
pinMode(B,9);
pinMode(E,10);
pinMode(D,11);
pinMode(C,12);
pinMode(dp,13);
 
}
 
void loop() {
 
counter();
/*change this field to control which
number you want to appear on the display.
counter - counts from 0-9
zero - shows zero
one - shows 1
two - shows 2
three - shows 3
four - shows 4
five - shows 5
six - shows 6
seven - shows 7
eight - shows 8
nine - shows 9
*/
 
}
 
void counter(){
zero();
delay(990);
one();
delay(990);
two();
delay(990);
three();
delay(990);
four();
delay(990);
five();
delay(990);
six();
delay(990);
seven();
delay(990);
eight();
delay(990);
nine();
delay(990);
ten();
delay(990);
eleven();
delay(990);
twelve();
delay(990);

}
 
void off(){ //turns off all lights
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, HIGH);
digitalWrite(F, HIGH);
digitalWrite(A, HIGH);
digitalWrite(B, HIGH);
digitalWrite(E, HIGH);
digitalWrite(D, HIGH);
digitalWrite(C, HIGH);
digitalWrite(dp, HIGH);
delay(10);
}
 
void zero(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, HIGH);
digitalWrite(F, LOW);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, LOW);
digitalWrite(D, LOW);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}
 
void one(){ //turns on
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, HIGH);
digitalWrite(F, HIGH);
digitalWrite(A, HIGH);
digitalWrite(B, LOW);
digitalWrite(E, HIGH);
digitalWrite(D, HIGH);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}
 
void two(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, LOW);
digitalWrite(F, HIGH);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, LOW);
digitalWrite(D, LOW);
digitalWrite(C, HIGH);
digitalWrite(dp, HIGH);
delay(10);
}
 
void three(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, LOW);
digitalWrite(F, HIGH);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, HIGH);
digitalWrite(D, LOW);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}
 
void four(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, LOW);
digitalWrite(F, LOW);
digitalWrite(A, HIGH);
digitalWrite(B, LOW);
digitalWrite(E, HIGH);
digitalWrite(D, HIGH);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}
 
void five(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, LOW);
digitalWrite(F, LOW);
digitalWrite(A, LOW);
digitalWrite(B, HIGH);
digitalWrite(E, HIGH);
digitalWrite(D, LOW);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}
 
void six(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, LOW);
digitalWrite(F, LOW);
digitalWrite(A, LOW);
digitalWrite(B, HIGH);
digitalWrite(E, LOW);
digitalWrite(D, LOW);
digitalWrite(C, LOW);
digitalWrite(dp, LOW);
delay(10);
}
 
void seven(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, HIGH);
digitalWrite(F, HIGH);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, HIGH);
digitalWrite(D, HIGH);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}
 
void eight(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, LOW);
digitalWrite(F, LOW);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, LOW);
digitalWrite(D, LOW);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}
 
void nine(){
digitalWrite(BB, HIGH);
digitalWrite(CC, HIGH);
digitalWrite(G, LOW);
digitalWrite(F, LOW);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, HIGH);
digitalWrite(D, HIGH);
digitalWrite(C, LOW);
digitalWrite(dp, LOW);
delay(10);
}

void ten(){
digitalWrite(BB, LOW);
digitalWrite(CC, LOW);
digitalWrite(G, HIGH);
digitalWrite(F, LOW);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, LOW);
digitalWrite(D, LOW);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}

void eleven(){
digitalWrite(BB, LOW);
digitalWrite(CC, LOW);
digitalWrite(G, HIGH);
digitalWrite(F, HIGH);
digitalWrite(A, HIGH);
digitalWrite(B, LOW);
digitalWrite(E, HIGH);
digitalWrite(D, HIGH);
digitalWrite(C, LOW);
digitalWrite(dp, HIGH);
delay(10);
}

void twelve(){
digitalWrite(BB, LOW);
digitalWrite(CC, LOW);
digitalWrite(G, LOW);
digitalWrite(F, HIGH);
digitalWrite(A, LOW);
digitalWrite(B, LOW);
digitalWrite(E, LOW);
digitalWrite(D, LOW);
digitalWrite(C, HIGH);
digitalWrite(dp, HIGH);
delay(10);
}
