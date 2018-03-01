#include <WString.h>

String incomingString = "";
int inputArray[9];

void setup() {
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  //Initialising the input array
  if (Serial.available() > 0) {
    //Not used
    //incomingString = Serial.readString();
  }
}

void loop() {
  
  // If receiving data:
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
