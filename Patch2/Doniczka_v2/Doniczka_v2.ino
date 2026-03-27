double water, sun;
int incomingByte = 0;
boolean read_marker;
int waterIndicator = A0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(9,OUTPUT);
}

void  loop() {
  //water = 0.4;
  //water = analogRead(waterIndicator);
  water = 1-(analogRead(waterIndicator)-241.0)/265.0;
  sun = 0.5;
  Serial.print("water_and_sun");
  Serial.print(" ");
  Serial.print(water);
  Serial.print(" ");
  Serial.print(sun);
  Serial.print("\n");
  delay(1000);
  char searchString[] = "Jump in!";
  read_marker = Serial.find(searchString);
  if(read_marker)
    digitalWrite(9,HIGH);
  else
    digitalWrite(9,LOW);
}
