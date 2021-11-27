#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

float Ax, Ay, Az;
float Qw,Qx,Qy,Qz;

/* This driver reads raw data from the BNO055

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3V DC
   Connect GROUND to common ground
   
*/

int button = 16; //D2(gpio4)
int buttonState=0;

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28);

/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  
  Serial.begin(115200);
  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
   pinMode(button, INPUT);
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
  // Possible vector values can be:
  // - VECTOR_ACCELEROMETER - m/s^2
  // - VECTOR_MAGNETOMETER  - uT
  // - VECTOR_GYROSCOPE     - rad/s
  // - VECTOR_EULER         - degrees
  // - VECTOR_LINEARACCEL   - m/s^2
  // - VECTOR_GRAVITY       - m/s^2

   buttonState=digitalRead(button); // put your main code here, to run repeatedly:
   
   uint8_t system, gyro, accel, mag = 0;
   bno.getCalibration(&system, &gyro, &accel, &mag);
   
   if (buttonState == 1){    
    if (accel == 3 && gyro == 3 && mag ==3){
      /* Display the floating point data */
      Serial.println("s");
      }
    
    else {
      Serial.print("CALIBRATION: Sys=");
      Serial.print(system, DEC);    
      Serial.print(" Gyro=");
      Serial.print(gyro, DEC);
      Serial.print(" Accel=");
      Serial.print(accel, DEC);
      Serial.print(" Mag=");
      Serial.println(mag, DEC);
      }

  }
  else if (buttonState==0) {
    /* Display calibration status for each sensor. */
    if (accel == 3 && gyro == 3 && mag ==3){
      imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
      imu::Quaternion quat = bno.getQuat();
      Qx = quat.x();
      Qy = quat.y();
      Qz = quat.z();
      Qw = quat.w();
      /* Display the floating point data */
      Serial.print(acc.x());
      Serial.print(',');
      Serial.print(acc.y());
      Serial.print(',');
      Serial.print(acc.z());
      Serial.print(',');
      Serial.print(Qw, 4);
      Serial.print(',');
      Serial.print(Qx, 4);
      Serial.print(',');
      Serial.print(Qy, 4);
      Serial.print(',');
      Serial.print(Qz, 4);
      Serial.println();
      }
    
    else {
      Serial.print("CALIBRATION: Sys=");
      Serial.print(system, DEC);    
      Serial.print(" Gyro=");
      Serial.print(gyro, DEC);
      Serial.print(" Accel=");
      Serial.print(accel, DEC);
      Serial.print(" Mag=");
      Serial.println(mag, DEC);
      }

  }
 delay(1);
}
