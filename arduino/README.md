# Arudino Readme

## Introduction

The main function of the ROV is to produce PWM signals to various actuators on the ROV. The values of the signals to output are communicated by UART interface from a Raspberry PI.

## PWM
The Arduino lists itself as having 13 PWM pins; upon testing it was found that most of these can be controlled and set to the values in the range for the main thruster motor.  
Here is an introduction on PWM and creating PWM signals in Arudinos: https://www.arduino.cc/en/Tutorial/SecretsOfArduinoPWM
