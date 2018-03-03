#include <WString.h>

String incomingString = "";
const int OUTPUT_ARRAY_SIZE = 10;
const int INPUT_ARRAY_SIZE = 1;
int outputArray[OUTPUT_ARRAY_SIZE];     //Array received from the Pi to control all outputs
int inputArray[INPUT_ARRAY_SIZE];     //Array of currently measured input values to send back to Pi
int arrayPointer=0;              // Int to point to current array position
String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete
boolean sendComplete = false;



void setup() {
  //Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  Serial.begin(115200);     // opens serial port, sets data rate to 115200 bps
  Serial.setTimeout(1000);     //The default timeout is a second - way too slow for our purposes. Now set to 1ms
  inputString.reserve(200); // reserve 200 bytes for the inputString
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);


  //For testing
inputArray[0] = 10000;
}

void loop() {
//==============================================COMMUNICATION===========================================
  //-----------------------------Check for incoming "output" values (eg: Thrusters)------------------------
  if (stringComplete) { //If new value received (ending in a newline character)

    int currentValue = inputString.toInt();
    
    if(currentValue == 11111 && arrayPointer != 0){
      arrayPointer = 0; //If sync value is not in position 0, reset to position 0
      //Serial.print("Sync error. Now reset to position 0."); //FOR DEBUGGING ONLY
    }
    
    outputArray[arrayPointer]= currentValue;

    // say what you got: 
    //Serial.print("[");
    //Serial.print(arrayPointer);
  //  Serial.print("]");
//    Serial.println(inputString); //FOR DEBUGGING ONLY

    if (arrayPointer==(OUTPUT_ARRAY_SIZE-1)){
      arrayPointer = 0; //Reset arraypointer if it's reached the maximum array position
      sendComplete = false; //Send back input values once all output values have been received
    }
    else{
      arrayPointer = arrayPointer + 1; //Else increment arrayPointer
    }

    //Reset input string and wait for new input
    inputString = "";
    stringComplete = false;
  }

  //------------------------------------Send input values back to Pi---------------------------------
  if (!sendComplete){ //If ready to send back values
    for(int i=0; i<INPUT_ARRAY_SIZE; i++) {
      //Serial.print("[");
      //Serial.print(i);
      //Serial.print("]");
      Serial.println(inputArray[i]);


      //For testing decrement  from 10000:
inputArray[0]=inputArray[0]-1;
      
    }
    sendComplete = true;
  }
//==============================================/COMMUNICATION===========================================

//==============================================READ_SENSORS===========================================



//==============================================/READ_SENSORS===========================================

//==============================================CONTROL_OUTPUTS===========================================

  if(outputArray[9]==1){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else{
      digitalWrite(LED_BUILTIN, LOW);
    }
 //==============================================/CONTROL_OUTPUTS===========================================

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
