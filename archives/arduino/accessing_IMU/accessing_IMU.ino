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
  // Accelerometer code
   IMU.setAccelFS(3);
   IMU.setAccelODR(5);
   IMU.setAccelOffset(-0.021957, -0.006711, 0.037808);
   IMU.setAccelSlope (0.994306, 0.994161, 1.000458);

   // Gyroscope code
   IMU.setGyroFS(2);
   IMU.setGyroODR(5);
   IMU.setGyroOffset (0.000000, 0.000000, 0.000000);
   IMU.setGyroSlope (1.194986, 1.180032, 1.125240);

   // Magnetometer code
   IMU.magnetUnit = MICROTESLA;  //   GAUSS   MICROTESLA   NANOTESLA
   IMU.setMagnetFS(0);
   IMU.setMagnetODR(8);
   IMU.setMagnetOffset(22.322998, -0.440674, -28.952637);
   IMU.setMagnetSlope (1.269114, 1.260585, 1.309950);
   
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
  //IMU.setMagnetFS(0); //   1=±800µT   2=±1200µT  3=±1600µT  Default= 0:±400 µT 
  
  
  // Change the sample frequency ( ODR = Output Dats rate)  
  // Note: setting 0..5 did not work on all systems. The default setting = 5 for compatibility reasons 
  //IMU.setMagnetODR(7);   // Sampling rate (0..8)->{0.625,1.25,2.5,5.0,10,20,40,80,400}Hz  
  //Serial.print(IMU.getMagnetODR());                       // alias IMU.magneticFieldSampleRate());
  Serial.println();
  //Serial.println(" Hz");
  

}

void loop() {

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(Ax, Ay, Az); //MEASURED IN G's

    Serial.print(Ax);
    Serial.print(',');
    Serial.print(Ay);
    Serial.print(',');
    Serial.print(Az);
    Serial.print(',');
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(Gx, Gy, Gz); //MEASURED IN DEGREES/s 
    
    Serial.print(Gx);
    Serial.print(',');
    Serial.print(Gy);
    Serial.print(',');
    Serial.print(Gz);
    Serial.print(',');
    //Serial.println();
  }

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(Mx, My, Mz); //MEASURED IN Gauss's 1x-4 Tesla

    Serial.print(Mx);
    Serial.print(',');
    Serial.print(My);
    Serial.print(',');
    Serial.print(Mz);
    Serial.println();
  }

delay(40); //need to delay for magnetometer

  }
