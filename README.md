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

