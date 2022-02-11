import sys
from time import sleep
import csv
import os
from unicodedata import name
sys.path.append('/home/mohamed/openzen/build')
import openzen

openzen.set_log_level(openzen.ZenLogLevel.Warning)

error, client = openzen.make_client()
if not error == openzen.ZenError.NoError:
    print ("Error while initializing OpenZen library")
    sys.exit(1)

error = client.list_sensors_async()

# check for events
sensor_desc_connect = None
while True:
    zenEvent = client.wait_for_next_event()

    if zenEvent.event_type == openzen.ZenEventType.SensorFound:
        print ("Found sensor {} on IoType {}".format( zenEvent.data.sensor_found.name,
            zenEvent.data.sensor_found.io_type))
        if sensor_desc_connect is None:
            sensor_desc_connect = zenEvent.data.sensor_found

    if zenEvent.event_type == openzen.ZenEventType.SensorListingProgress:
        lst_data = zenEvent.data.sensor_listing_progress
        print ("Sensor listing progress: {} %".format(lst_data.progress * 100))
        if lst_data.complete > 0:
            break
print ("Sensor Listing complete")

if sensor_desc_connect is None:
    print("No sensors found")
    sys.exit(1)
# connect to the first sensor found
error, sensor = client.obtain_sensor(sensor_desc_connect)

# or connect to a sensor by name
#error, sensor = client.obtain_sensor_by_name("LinuxDevice", "LPMSCU2000003")

if not error == openzen.ZenSensorInitError.NoError:
    print ("Error connecting to sensor")
    sys.exit(1)

print ("Connected to sensor !")

imu = sensor.get_any_component_of_type(openzen.component_type_imu)
if imu is None:
    print ("No IMU found")
    sys.exit(1)

## read bool property
error, is_streaming = imu.get_bool_property(openzen.ZenImuProperty.StreamData)
if not error == openzen.ZenError.NoError:
    print ("Can't load streaming settings")
    sys.exit(1)

print ("Sensor is streaming data: {}".format(is_streaming))
def runLoop():


    zenEvent = client.wait_for_next_event()

    # check if its an IMU sample event and if it
    # comes from our IMU and sensor component
    if zenEvent.event_type == openzen.ZenEventType.ImuData and \
        zenEvent.sensor == imu.sensor and \
        zenEvent.component.handle == imu.component.handle:

        imu_data = zenEvent.data.imu_data
    acc = imu_data.a
    return acc

def recordData(coordinate):
    dataX = []
    i = 0
    dir = str(os.path.abspath(os.curdir))
    print(dir)
    if coordinate == "+X":
        f = open(dir + "/lpmsData/posX.csv", "a+")
        writer = csv.writer(f, delimiter = ",")
        for i in range(1000):
            writer.writerow(runLoop())
            i+=1
        f.flush()
    if coordinate == "-X":
        f = open(dir + "/lpmsData/negX.csv", "a+")
        writer = csv.writer(f, delimiter = ",")
        for i in range(1000):
            writer.writerow(runLoop())
            i+=1
        f.flush()
    if coordinate == "+Y":
        f = open(dir + "/lpmsData/posY.csv", "a+")
        writer = csv.writer(f, delimiter = ",")
        for i in range(1000):
            writer.writerow(runLoop())
            i+=1
        f.flush()
    if coordinate == "-Y":
        f = open(dir + "/lpmsData/negY.csv", "a+")
        writer = csv.writer(f, delimiter = ",")
        for i in range(1000):
            writer.writerow(runLoop())
            i+=1
        f.flush()
    if coordinate == "+Z":
        f = open(dir + "/lpmsData/posZ.csv", "a+")
        writer = csv.writer(f, delimiter = ",")
        for i in range(1000):
            writer.writerow(runLoop())
            i+=1
        f.flush()
    if coordinate == "-Z":
        f = open(dir + "/lpmsData/negZ.csv", "a+")
        writer = csv.writer(f, delimiter = ",")
        for i in range(1000):
            writer.writerow(runLoop())
            i+=1
        f.flush()
    

recordData("-Z")
# print("first component done")
# sleep(8)
# recordData("-X")
# print("second component done")
# sleep(8)
# recordData("+Y")
# print("third component done")
# sleep(8)
# recordData("-Y")
# print("fourth component done")
# sleep(8)
# recordData("+Z")
# print("fifth component done")
# sleep(8)
# recordData("-Z")
# print("All done!")