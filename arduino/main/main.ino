#include <WString.h>

String incomingString = "";
const int ARRAYSIZE = 9;
int inputArray[ARRAYSIZE];

void setup() {
  //Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  Serial.begin(115200);     // opens serial port, sets data rate to 115200 bps
  Serial.setTimeout(1000);     //The default timeout is a second - way too slow for our purposes. Now set to 1ms
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
    for (int i=0; i<ARRAYSIZE; i++) {
      incomingString = Serial.readString();
      inputArray[i]=incomingString.toInt();
  
      // say what you got:
      //delay(5); //Delay to allow some time for the arduino to actually read the data
      
      //Serial.print("I received: ");
      Serial.print("[");
      Serial.print(i);
      Serial.print("]");
      Serial.println(incomingString);
    }
    
    //if(incomingString.toInt()==1){
    if(inputArray[8]==1){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else{
      digitalWrite(LED_BUILTIN, LOW);
    }
    

  }
}
