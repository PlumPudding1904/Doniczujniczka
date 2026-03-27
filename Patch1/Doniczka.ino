#include <TimeLib.h>
int czujnik_swiatla_1 = A0;
int czujnik_swiatla_2 = A1;
int czujnik_swiatla_3 = A2;
int czujnik_wody_1 = A3;
int czujnik_wody_2 = A4;
int czujnik_wody_3 = A5;
int LED1 = 1;
int LED2 = 2;
int LED3 = 3;
int LED4 = 4;
int LED5 = 5;
int LED6 = 6;
int LED7 = 7;
int LED8 = 8;
int LED9 = 9;
int LED10 = 10;
int minuta = 00;
int godzina = 16;
int dzien = 02;
int miesiac = 05;
int rok = 2023;
//
int natezenie_swiatla = 0;
int wilgotnosc = 0;
  
//int czujnik_wody_1 = A5;
//int czujnik_wody_2 = A6;

void setup() {
  Serial.begin(9600);        
  Serial.println("----  Test doniczka  ----");
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);      
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}
void ledy()
{
  if(wilgotnosc <= 205)
  {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, LOW);
    digitalWrite(LED3, LOW);
    digitalWrite(LED4, LOW);
    digitalWrite(LED5, LOW);
  }
  if(wilgotnosc > 205 && wilgotnosc < 410)
  {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, LOW);
    digitalWrite(LED4, LOW);
    digitalWrite(LED5, LOW);
  }
  if(wilgotnosc >= 410 && wilgotnosc < 615)
  {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, HIGH);
    digitalWrite(LED4, LOW);
    digitalWrite(LED5, LOW);
  }
  if(wilgotnosc >= 615 && wilgotnosc < 820)
  {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, HIGH);
    digitalWrite(LED4, HIGH);
    digitalWrite(LED5, LOW);
  }
  if(wilgotnosc >= 820 && wilgotnosc <= 1023)
  {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, HIGH);
    digitalWrite(LED4, HIGH);
    digitalWrite(LED5, HIGH);
  }
  /*
  if(natezenie_swiatla <= 1023 && natezenie_swiatla > 820)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, LOW);
    digitalWrite(LED8, LOW);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  if(natezenie_swiatla <= 820 && natezenie_swiatla > 615)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, LOW);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  if(natezenie_swiatla <= 615 && natezenie_swiatla > 410)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  if(natezenie_swiatla <= 410 && natezenie_swiatla < 205)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, HIGH);
    digitalWrite(LED10, LOW);
  }
  if(natezenie_swiatla <= 205)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, HIGH);
    digitalWrite(LED10, HIGH);
  }  
*/
if(natezenie_swiatla <= 205)
  {
    Serial.print(natezenie_swiatla);
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, LOW);
    digitalWrite(LED8, LOW);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  else if(natezenie_swiatla > 205 && natezenie_swiatla < 410)
  {
    Serial.print(natezenie_swiatla);
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, LOW);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  else if(natezenie_swiatla >= 410 && natezenie_swiatla < 615)
  {
    Serial.print(natezenie_swiatla);
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  else if(natezenie_swiatla >= 615 && natezenie_swiatla < 820)
  {
    Serial.print(natezenie_swiatla);
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, HIGH);
    digitalWrite(LED10, LOW);
  }
  else if(natezenie_swiatla >= 820 && natezenie_swiatla <= 1023)
  {
    Serial.print(natezenie_swiatla);
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, HIGH);
    digitalWrite(LED10, HIGH);
  }
}

void czas()
 {
  Serial.print(day(now()));
  Serial.print("/");
  Serial.print(month(now()));
  Serial.print("/");
  Serial.print(year(now()));
  Serial.print(" ");
  Serial.print(hour(now()));
  Serial.print(":");
  Serial.print(minute(now()));
 }

void obsluga()
{
  minuta+=10; 
  if(minuta==60)
  {
    godzina+=1;
    minuta=0;
  }
  if(godzina==24)
  {
    dzien+=1;
    godzina=0;
  }
  
}

void loop() 
{

  setTime(godzina,minuta,00,dzien,miesiac,rok);
  natezenie_swiatla = (analogRead(czujnik_swiatla_1)+analogRead(czujnik_swiatla_2)+analogRead(czujnik_swiatla_3))/3;
  wilgotnosc = (analogRead(czujnik_wody_1)+analogRead(czujnik_wody_2)+analogRead(czujnik_wody_3))/3;
  czas();
  Serial.print(" ");
  Serial.print(natezenie_swiatla); 
  Serial.print(" ");
  Serial.print(wilgotnosc);
  Serial.println("");
  Serial.print(analogRead(czujnik_swiatla_1)); 
  Serial.println("");
  Serial.print(analogRead(czujnik_swiatla_2)); 
  Serial.println("");
  Serial.print(analogRead(czujnik_swiatla_3)); 
  Serial.println("");
  Serial.print(analogRead(czujnik_wody_1)); 
  Serial.println("");
  Serial.print(analogRead(czujnik_wody_2)); 
  Serial.println("");
  Serial.print(analogRead(czujnik_wody_3)); 
  Serial.println("");
  obsluga();
  ledy();
  delay(1000);                       
}
