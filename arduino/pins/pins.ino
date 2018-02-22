#ifndef _PINS_
#define _PINS_

#include <Servo.h>

// 1500ms +/- 400ms
#define SERVO_MIN_PERIOD_MUS 1100
#define SERVO_MAX_PERIOD_MUS 1900

#define TOPINDEX 0;
#define FORELEFTINDEX 1
#define FORERIGHTINDEX 2
#define AFTLEFTINDEX 3
#define AFTRIGHTINDEX 4

byte servoMappings [] = {0,1,2,3,4};
Servo servo[5];


void setup() {
    for (size_t i = 0; i < 5; i++) {
        servo[i].attach(servoMappings[i], SERVO_MIN_PERIOD_MUS, SERVO_MAX_PERIOD_MUS);
        servo[i].writeMicroseconds(1500); // send "stop" signal to ESC.
    }
    delay(1000); // delay to allow the ESC to recognize the stopped signal
}

void loop() {
    int signal = 1700; // Set signal value, which should be between 1100 and 1900
    servo[0].writeMicroseconds(signal); // Send signal to ESC.
}

void setServoForeLeft(int a) {
    if (a <= SERVO_MIN_PERIOD_MUS) {
        a = SERVO_MIN_PERIOD_MUS;
    }
    if (a >SERVO_MAX_PERIOD_MUS) {
        a =SERVO_MAX_PERIOD_MUS;
    }
    servo[servoMappings[FORELEFTINDEX]].writeMicroseconds(a);
}
#endif
