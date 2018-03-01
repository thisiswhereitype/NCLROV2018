#include <WString.h>
//int incomingByte = 0;   // for incoming serial data
//char incomingString[] = "";
String incomingString = "";

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
    incomingString = Serial.readString();

//    if(incomingString=="test"){
//      digitalWrite(LED_BUILTIN, HIGH);
//      delay(1000);
//      digitalWrite(LED_BUILTIN, LOW);
//    }

    // say what you got:
    delay(5); //Delay to allow some time for the arduino to actually read the data
    
    Serial.print("I received: ");
    Serial.println(incomingString);
  }
}
