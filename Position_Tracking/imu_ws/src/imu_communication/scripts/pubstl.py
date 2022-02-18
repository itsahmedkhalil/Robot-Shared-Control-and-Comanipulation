#!/usr/bin/env python
# license removed for brevity

from getch import getch, pause
import rospy
from std_msgs.msg import Float64
from imu_communication.msg import Num
from visualization_msgs.msg import Marker
from time import time
from geometry_msgs.msg import Accel
from tf import TransformBroadcaster
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import random
import sys
sys.path.append('/home/mohamed/openzen/build')
#sys.path.append('/home/ahmedkhalil/openzen')
import openzen
#sys.path.append("/home/mohamed/imu_ws/devel/opencv_tools/lib/python3.8/site-packages/opencv_tools")
#from kalman2 import Kalman
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

    print("Sensor is streaming data: {}".format(is_streaming))


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
    b = TransformBroadcaster()
    translation = (0.0, 0.0, 0.0)
    rotation = (0.0, 0.0, 0.0, 1.0)
    rate = rospy.Rate(500)

    calibratedData = []
    vel = [0, 0, 0]

    damp = 1

    # Initialize the publisher for the marker
    marker_pub = rospy.Publisher(
        "/visualization_marker", Marker, queue_size=1)
    marker = Marker()
    marker.header.frame_id = "world"
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    # marker initial position
    marker.pose.position.x = 0
    marker.pose.position.y = 0
    marker.pose.position.z = 0

    # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
    marker.type = 1
    marker.id = 0
    # Set the scale of the marker
    marker.scale.x = 0.05
    marker.scale.y = 0.05
    marker.scale.z = 0.05
    # Set the color
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    #w = tk.Tk()
    print("Calibration Started")
    acc_publisher = rospy.Publisher('/acc', Accel, queue_size=1)
    acc_msg = Accel()

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
                calibratedData.append(cal_acc)  # cal_acc
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
    counter = 0
    x_n = np.zeros(3)
    x_n_1 = np.zeros(3)
    x_n_2 = np.zeros(3)
    t_old = float(time())
   #traformation matrix from state parameters to measurement domain

    Q = 0.02*np.identity(6) #covariance/error of process
    #R = 5*np.identity(3) #0.3 covariance/error of measurement
    x_hat_k = np.array([[0,0,0,0,0,0]]).T # x_t = [T,q,T_dot]
    P_k = 100*np.identity(6)
    #kalman = Kalman(R, Q)
    while not rospy.is_shutdown():
        try:
            

            zenEvent = client.wait_for_next_event()

            # check if its an IMU sample event and if it
            # comes from our IMU and sensor component
            if zenEvent.event_type == openzen.ZenEventType.ImuData and \
                    zenEvent.sensor == imu.sensor and \
                    zenEvent.component.handle == imu.component.handle:

                imu_data = zenEvent.data.imu_data

            t = float(time())
            acc = np.array(imu_data.a) 
            quat = imu_data.q
            #quat = quat.inverse()
            r = R.from_quat([-quat[1], -quat[2], -quat[3], quat[0]])
            r_acc = r.apply(acc)
            r_acc = (r_acc + np.array([0, 0, 1]))*9.81
 

            acc_msg.angular.x = r_acc[0]
            acc_msg.angular.y = r_acc[1]
            acc_msg.angular.z = r_acc[2]
            dt = t - t_old
            #x_hat_k, P_k = kalman.predict(x_hat_k, P_k, dt)
           # x_hat_k, P_k = kalman.update(x_hat_k, P_k, r_acc)
            #acc_msg.linear.x = x_hat_k[0][0]
            #acc_msg.linear.y = x_hat_k[1][0]
            #acc_msg.linear.z = x_hat_k[2][0]
            # print(1/dt)
            #r_acc_F = 0.22826091*r_acc_F_1 + 0.00307065*r_acc+0.00307065*r_acc_1
            # for i in range(len(r_acc))    :
            #     if abs(r_acc[i]) < 0.005:
            #         r_acc[i] = 0
            #         damp[i] = damp_high
            #         #damp = 200
            #     else:
            #         damp[i] =  damp_low
            # if abs(r_acc[0]) < 0.01:
            #     r_acc[0] = 0
            #     damp[0] = damp_high
            # else:
            #     damp[0] = damp_low
            # if abs(r_acc[1]) < 0.01:
            #     r_acc[1] = 0
            #     damp[1] = damp_high
            # else:
            #     damp[1] = damp_low

            """If the median of the last X values of velocity is greater than 0 and very close to 0 
            then the velocity is clipped between positive
            velocity values and zero for a specific time period."""
            """If the median of the last X values of velocity is less than 0 and very close to 0 
            then the velocity is clipped between negative
            velocity values and zero for a specific time period.
            Have to make a scatter plot for velocity values"""
            vel = (vel + r_acc*dt)/(1+damp*dt)
            # for v in range(len(vel)):
            #     if abs(vel[v]) < 0.0005:
            #         # j = 0
            #         # if j < 600:
            #         vel[v] = 0
            #            # j += 1
            #     else:
            #         vel[v] = (vel[v] + r_acc[v]*dt)/(1+damp[v]*dt)
            # print(r_acc)
            # print(vel)
            #x_n = x_n_1 + dt*vel

            # for i in range(len(r_acc)):

            x_n = (2*x_n_1 - x_n_2 + damp*x_n_1*dt+r_acc*dt*dt)/(damp*dt+1)
            # vel = vel + r_acc*dt
            # dist = (dist + vel*dt)
            # r_acc_last = r_acc
            # print(np.linalg.norm(r_acc))
            #print(x_n[0], x_n[1], x_n[2])
                #translation = (x_n)

            translation = (x_n[0],x_n[1],x_n[2])#(-x_n[0],-x_n[1],-x_n[2])  # x_n[2])
            rotation = (-quat[1], -quat[2], -quat[3], quat[0])

            # marker distance between imu and marker
            delta_distX = abs(x_n[0] - marker.pose.position.x)
            #delta_distY = abs(x_n[1] - marker.pose.position.y)
            #delta_distZ = abs(x_n[2] - marker.pose.position.z)

            # if the distance is cloes to 0, the marker move to a random position
            if delta_distX < 0.05:  # and delta_distY < 0.15:
                counter += 1
                marker.pose.position.x = float(random.randint(-5, 5))/20
                marker.pose.position.y = 0  # float(random.randint(-10,10))/10
                print("new marker position:",
                      marker.pose.position.x, marker.pose.position.y)
                marker.pose.position.z = 0
                print("you got number of points! :", counter)

            else:
                pass
                       
            marker_pub.publish(marker)
            # rospy.loginfo(np.linalg.norm(r_acc))
            b.sendTransform(translation, rotation,
                            Time.now(), 'imu', '/world')
            # rospy.loginfo(marker)
            t_old = t
            x_n_2 = x_n_1
            x_n_1 = x_n
            acc_publisher.publish(acc_msg)

        except Exception as e:
            #t = float(time())
            print(e)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('my_broadcaster')
    runLoop()
    rospy.spin
