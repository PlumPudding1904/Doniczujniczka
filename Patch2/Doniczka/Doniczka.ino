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
//
double natezenie_swiatla = 0;
double wilgotnosc = 0;
boolean read_marker;
  
//int czujnik_wody_1 = A5;
//int czujnik_wody_2 = A6;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);     
  //Serial.println("----  Test doniczka  ----");
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
void ledy_wilgotnosc()
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
}
void ledy_natezenie_swiatla()
{
  if(natezenie_swiatla <= 205)
    {
      digitalWrite(LED6, HIGH);
      digitalWrite(LED7, LOW);
      digitalWrite(LED8, LOW);
      digitalWrite(LED9, LOW);
      digitalWrite(LED10, LOW);
    }
  else if(natezenie_swiatla > 205 && natezenie_swiatla < 410)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, LOW);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  else if(natezenie_swiatla >= 410 && natezenie_swiatla < 615)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, LOW);
    digitalWrite(LED10, LOW);
  }
  else if(natezenie_swiatla >= 615 && natezenie_swiatla < 820)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, HIGH);
    digitalWrite(LED10, LOW);
  }
  else if(natezenie_swiatla >= 820 && natezenie_swiatla <= 1023)
  {
    digitalWrite(LED6, HIGH);
    digitalWrite(LED7, HIGH);
    digitalWrite(LED8, HIGH);
    digitalWrite(LED9, HIGH);
    digitalWrite(LED10, HIGH);
  }
}

void loop() 
{
  natezenie_swiatla = (analogRead(czujnik_swiatla_1)+analogRead(czujnik_swiatla_2)+analogRead(czujnik_swiatla_3))/3;
  wilgotnosc = (analogRead(czujnik_wody_1)+analogRead(czujnik_wody_2)+analogRead(czujnik_wody_3))/3;
  ledy_natezenie_swiatla();
  wilgotnosc = wilgotnosc/1023.0;
  natezenie_swiatla = natezenie_swiatla/1023.0;
  Serial.print("water_and_sun");
  Serial.print(" ");
  Serial.print(wilgotnosc); 
  Serial.print(" ");
  Serial.print(natezenie_swiatla);
  Serial.print("\n");
  char searchString[] = "Jump in!";
  read_marker = Serial.find(searchString);
  if(read_marker){
    digitalWrite(5,HIGH);}
    else{
     digitalWrite(5,LOW);}
  delay(1000);                       
}
