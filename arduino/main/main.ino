#include <WString.h>
//int incomingByte = 0;   // for incoming serial data
char incomingString[] = "";

void setup() {
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    //incomingString = Serial.readString().toCharArray();
    Serial.readBytes(incomingString,4);

    if(incomingString=="test"){
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000);
      digitalWrite(LED_BUILTIN, LOW);
    }
    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingString);
  }
}
