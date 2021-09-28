/* 
 Arduino LSM9DS1 - Accelerometer Application3
This example reads the acceleration values as relative direction and degrees,5  from the LSM9DS1 sensor and prints them to the Serial Monitor or Serial Plotter.6
7  The circuit:8  - Arduino Nano 33 BLE9
10  Created by Riccardo Rizzo11
12  Modified by Jose García13  27 Nov 202014
15  This example code is in the public domain.*/
#include <Arduino_LSM9DS1.h>

float Ax, Ay, Az;
float Gx, Gy, Gz;

void setup() {
  Serial.begin(9600);

  while(!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  
  //Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());  
  Serial.print(',');
  //Serial.print("Hz"); 

  //Serial.print("Gyroscope sample rate = ");  
  Serial.print(IMU.gyroscopeSampleRate());
  //Serial.print("Hz");

  Serial.println();

}

void loop() {

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(Ax, Ay, Az);

    Serial.print(Ax);
    Serial.print(',');
    Serial.print(Ay);
    Serial.print(',');
    Serial.print(Az);
    Serial.print(',');
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(Gx, Gy, Gz);
    
    Serial.print(Gx);
    Serial.print(',');
    Serial.print(Gy);
    Serial.print(',');
    Serial.print(Gz);
    Serial.println();
  }

delay(6000);

  }
