# Robot-Shared-Control-and-Comanipulation

**Running Arduino_BLE**
---

1. Arduino

    + Download the LSM9DS1 V2 Library from here: https://github.com/FemmeVerbeek/Arduino_LSM9DS1/blob/master/Getting%20Started.md 
        - Even if you have LSM9DS1 installed, you might not have the correct version
    + Upload the test.ino code to your Arduino Nano
        - Open the Serial Monitor and copy the MAC address being displayed
    + Move onto Python

2. Python

    + Run the test.py script in your terminal by running the following:
    	- `$ python3 test.py [MAC ADDRESS FROM ARDUINO]`

3. RVIZ
    + Access ROS WS
        - `$ cd Position_Tracking/imu_ws/`

    + Change permissions for Python script
        - `$ roscd imu_communication/scripts/`
        - `$ sudo chmod +x pub.py`

    + Change permissions for Launch file
        - `$ roscd imu_communication/launch/`
        - `$ sudo chmod +x rviz.launch`

    + Run the launch file
        - `$ roslaunch imu_communication rviz.launch`

**Using live plotting**
---

1. Connect your Arduino to your computer via USB and make a note of the port name

2. Go to the arduino tracjectory and upload rawdata2BN0_2 to your Arduino
    - `$ cd Position_Tracking/arduino`

3. Open the serial monitor and ensure that each of the calibration values are equal to 3
    - Keep the arduino stationary at the start, this is to calibrate the gyroscopre
    - Rotate the arduino across each x, y, and z axis, this is to calibrate the magnetometer
    - Tilt the arduino at a 45 degree in the x-axis. Place the arduino on a flat surface. Repeat for each of the axis until it is calibrated. 
    
4. Once, it is fully calibrated, go to python directory
    - `$ cd Position_Tracking/python` 

5. Run the plotting.py script in your terminal
    - Alter the code accordingly so you could graph the states that you want

- Note: If the IMU is not calibrated, the graphs will stop plotting any new values