#!/usr/bin/env python
# license removed for brevity
import rospy
import serial
import os
from imu_communication.msg import Imu
from time import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import random
import sys
sys.path.append('/home/mohamed/openzen/build')
# sys.path.append('/home/ahmedkhalil/openzen')
import openzen


def main(): 
    imuPub = rospy.Publisher("/imu_data", Imu, queue_size=1)
    rospy.init_node("imu_publisher")
    rate = rospy.Rate(300)
    imu_raw = Imu()
    imu_raw.linearaccel.x = 0
    imu_raw.linearaccel.y = 0
    imu_raw.linearaccel.z = 0
    imu_raw.acceleration.x = 0
    imu_raw.acceleration.y = 0
    imu_raw.acceleration.z = 0
    imu_raw.orientation.x = 0
    imu_raw.orientation.y = 0
    imu_raw.orientation.z = 0
    imu_raw.orientation.w = 1
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

    calibratedData = []
    for i in range(400):
        zenEvent = client.wait_for_next_event()

        # check if its an IMU sample event and if it
        # comes from our IMU and sensor component
        if zenEvent.event_type == openzen.ZenEventType.ImuData and \
            zenEvent.sensor == imu.sensor and \
            zenEvent.component.handle == imu.component.handle:

            imu_data = zenEvent.data.imu_data
        acc_init = np.array(imu_data.a)*9.81
        calibratedData.append(acc_init)
        i+=1
    np_calibratedData = np.array(calibratedData)
    g = np.sum(np.linalg.norm(np_calibratedData, axis=1)/np.shape(np_calibratedData)[0])
    #     print("Calibration Completed")
    # start streaming data

    dir = os.path.dirname(os.path.realpath(__file__))[:-7] #[:-8]
    M = np.load(dir + 'data' + '/sensitivity.npy')
    b_a = np.load(dir + 'data' + '/offset.npy')
    #print(M)
    #print(b_a)
    while not rospy.is_shutdown():
        try:
            zenEvent = client.wait_for_next_event()

            # check if its an IMU sample event and if it
            # comes from our IMU and sensor component
            if zenEvent.event_type == openzen.ZenEventType.ImuData and \
                zenEvent.sensor == imu.sensor and \
                zenEvent.component.handle == imu.component.handle:

                imu_data = zenEvent.data.imu_data
            acc = np.array(imu_data.a)
            acc_r = acc.reshape(3,1)
            diff =  (acc_r - b_a)
            acc_hat = np.dot(np.linalg.inv(M),diff)
            #print(acc_hat)
            #print(acc_hat)
            acc_hat = acc_hat.reshape(3)
            #print(acc_hat)
            acc_hat = np.asarray(acc_hat)
            quat = np.array(imu_data.q)
            r = R.from_quat([quat[1],quat[2],quat[3],-quat[0]])
            r_acc = r.apply(acc_hat)
            r_acc = r_acc + np.array([0, 0, g])
            imu_raw.time = rospy.get_time()
            imu_raw.acceleration.x = acc[0]
            imu_raw.acceleration.y = acc[1]
            imu_raw.acceleration.z = acc[2]
            imu_raw.linearaccel.x = acc_hat[0]
            imu_raw.linearaccel.y = acc_hat[1]
            imu_raw.linearaccel.z = acc_hat[2]
            imu_raw.orientation.w = -quat[0]
            imu_raw.orientation.x = quat[1]
            imu_raw.orientation.y = quat[2]
            imu_raw.orientation.z = quat[3]
            print(acc)
            #imu_raw.stamp = rospy.Time.now()
            imuPub.publish(imu_raw)
        except rospy.ROSInterruptException:
            pass
        rate.sleep()


if __name__ == '__main__':
    main()