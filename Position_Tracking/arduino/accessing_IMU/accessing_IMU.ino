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
float Mx, My, Mz;

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
  Serial.print(',');
  //Serial.print("Hz");
  
  // note the FS value does not change the output of the read method, it just assigns more bits to the chip output,
  // increasing accuracy at the cost of a smaller range 
  IMU.setMagnetFS(0); //   1=±800µT   2=±1200µT  3=±1600µT  Default= 0:±400 µT 
  IMU.magnetUnit = MICROTESLA;  //   GAUSS   MICROTESLA   NANOTESLA
  
  // Change the sample frequency ( ODR = Output Dats rate)  
  // Note: setting 0..5 did not work on all systems. The default setting = 5 for compatibility reasons 
  IMU.setMagnetODR(7);   // Sampling rate (0..8)->{0.625,1.25,2.5,5.0,10,20,40,80,400}Hz  
  Serial.print(IMU.getMagnetODR());                       // alias IMU.magneticFieldSampleRate());
  Serial.println();
  //Serial.println(" Hz");
  

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
    Serial.print(',');
  }

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(Mx, My, Mz);

    Serial.print(Mx);
    Serial.print(',');
    Serial.print(My);
    Serial.print(',');
    Serial.print(Mz);
    Serial.println();
  }

delay(40); //need to delay for magnetometer

  }
