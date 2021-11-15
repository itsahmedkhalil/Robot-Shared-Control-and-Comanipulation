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

int LED =9; // led light at pin 9
const int BUTTON = 4; // Naming switch button pin
int BUTTONstate = 0; // A variable to store Button Status / Input

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

  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  pinMode (BUTTON, INPUT);
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

  BUTTONstate = digitalRead(BUTTON);  // Reading button status / input

  
  
  if (BUTTONstate == HIGH) {    
    Ax = 0;
    Ay = 0;
    Az = 0;  
  }
  else {
    imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
    imu::Quaternion quat = bno.getQuat();
    Ax = acc.x();
    Ay = acc.y();
    Az = acc.z();
    Qx = quat.x();
    Qy = quat.y();
    Qz = quat.z();
    Qw = quat.w();
  }

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

  if (accel == 3 && mag == 3){
    digitalWrite(LED, HIGH);
  
    /* Display the floating point data */
    Serial.print(Ax);
    Serial.print(',');
    Serial.print(Ay);
    Serial.print(',');
    Serial.print(Az);
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
    digitalWrite(LED, LOW);
    }
  
  delay(10);
}
