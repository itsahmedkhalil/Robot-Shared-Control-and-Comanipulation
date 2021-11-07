#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

float Ax, Ay, Az;
float Gx, Gy, Gz;
float Mx, My, Mz;

/* This driver reads raw data from the BNO055

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3V DC
   Connect GROUND to common ground
   
*/

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
  imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  imu::Vector<3> gyr = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  imu::Vector<3> magn = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);  
  imu::Quaternion quat = bno.getQuat();

  Ax = acc.x();
  Ay = acc.y();
  Az = acc.z();

  Mx = magn.x();
  My = magn.y();
  Mz = magn.z();

  Gx = gyr.x();
  Gy = gyr.y();
  Gz = gyr.z();
  
  /* Display the floating point data */
  Serial.print(String(Ax));
  Serial.print(',');
  Serial.print(String(Ay));
  Serial.print(',');
  Serial.print(String(Az));
  Serial.print(',');
  Serial.print(String(Gx));
  Serial.print(',');
  Serial.print(String(Gy));
  Serial.print(',');
  Serial.print(String(Gz));
  Serial.print(',');
  Serial.print(String(Mx));
  Serial.print(',');
  Serial.print(String(My));
  Serial.print(',');
  Serial.print(String(Mz));
  Serial.print(',');
  //Serial.println();
  
  Serial.print(quat.w(), 4);
  Serial.print(',');
  Serial.print(quat.x(), 4);
  Serial.print(',');
  Serial.print(quat.y(), 4);
  Serial.print(',');
  Serial.print(quat.z(), 4);
  Serial.println();
  

  /* Display calibration status for each sensor. */
    uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);
  Serial.print("CALIBRATION: Sys=");
  Serial.print(system, DEC);
  Serial.print(" Gyro=");
  Serial.print(gyro, DEC);
  Serial.print(" Accel=");
  Serial.print(accel, DEC);
  Serial.print(" Mag=");
  Serial.println(mag, DEC);

  delay(10);
}
