#include <WString.h>

String incomingString = "";
const int ARRAYSIZE = 10;
int inputArray[ARRAYSIZE];
int arrayPointer=0;              // Int to point to current array position
String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete

void setup() {
  //Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  Serial.begin(115200);     // opens serial port, sets data rate to 115200 bps
  Serial.setTimeout(1000);     //The default timeout is a second - way too slow for our purposes. Now set to 1ms
  inputString.reserve(200); // reserve 200 bytes for the inputString
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (stringComplete) { //If new value received (ending in a newline character)

    int currentValue = inputString.toInt();
    
    //currentValue = 11111;
    if(currentValue == 11111 && arrayPointer != 0){
      arrayPointer = 0; //If sync value is not in position 0, reset to position 0
      Serial.print("Sync error. Now reset to position 0.");
    }
    
    inputArray[arrayPointer]= currentValue;

    // say what you got:
    
    Serial.print("[");
    Serial.print(arrayPointer);
    Serial.print("]");
    Serial.println(inputString);

    if (arrayPointer==(ARRAYSIZE-1)){
      arrayPointer = 0; //Reset arraypointer if it's reached the maximum array position
    }
    else{
      arrayPointer = arrayPointer + 1; //Else increment arrayPointer
    }

    //Reset input string and wait for new input
    inputString = "";
    stringComplete = false;
  }



  if(inputArray[8]==1){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else{
      digitalWrite(LED_BUILTIN, LOW);
    }
  // If receiving data:
//  if (Serial.available() > 0) {
//
//    for (int i=0; i<ARRAYSIZE; i++) {
//      incomingString = Serial.readString();
//      inputArray[i]=incomingString.toInt();
//  
//      // say what you got:
//      //delay(5); //Delay to allow some time for the arduino to actually read the data
//      
//      //Serial.print("I received: ");
//      Serial.print("[");
//      Serial.print(i);
//      Serial.print("]");
//      Serial.println(incomingString);
//    }
//    
//    //if(incomingString.toInt()==1){
//    if(inputArray[8]==1){
//      digitalWrite(LED_BUILTIN, HIGH);
//    }
//    else{
//      digitalWrite(LED_BUILTIN, LOW);
//    }
//  }
}



/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
