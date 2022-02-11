
from getch import getch, pause
import rospy
from imu_communication.msg import state
from imu_communication.msg import Num
from visualization_msgs.msg import Marker
from time import time
from geometry_msgs.msg import Pose
from tf import TransformBroadcaster
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import sys
sys.path.append('/home/ahmedkhalil/openzen')
import openzen


openzen.set_log_level(openzen.ZenLogLevel.Warning)
error, client = openzen.make_client()
if not error == openzen.ZenError.NoError:
    print("Error while initializing OpenZen library")
    sys.exit(1)

error = client.list_sensors_async()




# check for events
sensor_desc_connect = None
while True:
    zenEvent = client.wait_for_next_event()

    if zenEvent.event_type == openzen.ZenEventType.SensorFound:
        print("Found sensor {} on IoType {}".format(zenEvent.data.sensor_found.name,
                                                    zenEvent.data.sensor_found.io_type))
        if sensor_desc_connect is None:
            sensor_desc_connect = zenEvent.data.sensor_found

    if zenEvent.event_type == openzen.ZenEventType.SensorListingProgress:
        lst_data = zenEvent.data.sensor_listing_progress
        print("Sensor listing progress: {} %".format(lst_data.progress * 100))
        if lst_data.complete > 0:
            break
print("Sensor Listing complete")

if sensor_desc_connect is None:
    print("No sensors found")
    sys.exit(1)
# connect to the first sensor found
error, sensor = client.obtain_sensor(sensor_desc_connect)

# or connect to a sensor by name
#error, sensor = client.obtain_sensor_by_name("LinuxDevice", "LPMSCU2000003")

if not error == openzen.ZenSensorInitError.NoError:
    print("Error connecting to sensor")
    sys.exit(1)

print("Connected to sensor !")

imu = sensor.get_any_component_of_type(openzen.component_type_imu)
if imu is None:
    print("No IMU found")
    sys.exit(1)

# read bool property
error, is_streaming = imu.get_bool_property(openzen.ZenImuProperty.StreamData)
if not error == openzen.ZenError.NoError:
    print("Can't load streaming settings")
    sys.exit(1)

#print("Sensor is streaming data: {}".format(is_streaming))


def runLoop():
    # load the alignment matrix from the sensor
    # some sensors don't support this (for example IG1, BE1)
    #error, accAlignment = imu.get_array_property_float(openzen.ZenImuProperty.AccAlignment)
    # if not error == openzen.ZenError.NoError:
    #    print ("Can't load alignment")
    #    sys.exit(1)

    # if not len(accAlignment) == 9:
    #    print ("Loaded Alignment has incosistent size")
    #    sys.exit(1)

    #print ("Alignment loaded: {}".format(accAlignment))

    # store float array
    #error = imu.set_array_property_float(openzen.ZenImuProperty.AccAlignment, accAlignment)

    # if not error == openzen.ZenError.NoError:
    #    print ("Can't store alignment")
    #    sys.exit(1)

    #print("Stored alignment {} to sensor".format(accAlignment))

    # start streaming data

    # Your serial port might be different!

    rate = rospy.Rate(500)

    calibratedData = []
    vel = [0, 0, 0]

    damp = 1

    print("Calibration Started")
    state_publisher = rospy.Publisher('/state', state, queue_size=1)
    state_msg = state()

    try:
        for i in range(400):
            zenEvent = client.wait_for_next_event()

            # check if its an IMU sample event and if it
            # comes from our IMU and sensor component
            if zenEvent.event_type == openzen.ZenEventType.ImuData and \
                    zenEvent.sensor == imu.sensor and \
                    zenEvent.component.handle == imu.component.handle:

                imu_data = zenEvent.data.imu_data
                acc_init = np.array(imu_data.a)
                quat_init = imu_data.q
                r_init = R.from_quat(
                    [quat_init[1], quat_init[2], quat_init[3], quat_init[0]])
                cal_acc = r_init.apply(acc_init)
                calibratedData.append(cal_acc)  # cal_acc)
                i += 1
            pass
        np_calibratedData = np.array(calibratedData)
        g = np.sum(np.linalg.norm(np_calibratedData, axis=1) /
                   np.shape(np_calibratedData)[0])
        print(g)
        print("Calibration Completed")
    except Exception as e:
        print(e)
        g = 9.81
    print("Gravity: ", g)

    vel = np.zeros(3)
    x_n = np.zeros(3)
    x_n_1 = np.zeros(3)
    x_n_2 = np.zeros(3)
    t_old = float(time())
    while not rospy.is_shutdown():
        try:
            t = float(time())

            zenEvent = client.wait_for_next_event()

            # check if its an IMU sample event and if it
            # comes from our IMU and sensor component
            if zenEvent.event_type == openzen.ZenEventType.ImuData and \
                    zenEvent.sensor == imu.sensor and \
                    zenEvent.component.handle == imu.component.handle:

                imu_data = zenEvent.data.imu_data
            

            acc = np.array(imu_data.a) 
            quat = imu_data.q
            quat[0] = -quat[0]
            r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
            r_acc = r.apply(acc)
            r_acc = (r_acc + np.array([0, 0, 1]))*9.81
 
         
            dt = t - t_old

            vel = (vel + r_acc*dt)/(1+damp*dt)

            x_n = (2*x_n_1 - x_n_2 + damp*x_n_1*dt+r_acc*dt*dt)/(damp*dt+1)
            
            t_old = t
            x_n_2 = x_n_1
            x_n_1 = x_n
    
            state_msg.position = x_n
            #state_msg.velocity = vel
            #state_msg.acceleration = r_acc
            state_msg.orientation = quat
            state_publisher.publish(state_msg)

        except Exception as e:
            #t = float(time())
            print(e)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('my_broadcaster')
    runLoop()
    rospy.spin
