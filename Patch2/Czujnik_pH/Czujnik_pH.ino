double fertilizer;
boolean read_marker;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(9,OUTPUT);
}

void  loop() {
  fertilizer = 6.5;
  char searchString[] ="Gimme pH!";// reading!";
  read_marker = Serial.find(searchString);
  //if(read_marker)
  //{
    Serial.print("fertilizer");
    Serial.print(" ");
    Serial.print(fertilizer);
    Serial.print("\n");
    delay(1000);
  //}
}
