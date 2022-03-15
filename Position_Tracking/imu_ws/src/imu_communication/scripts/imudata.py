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
    imuPub = rospy.Publisher("/imu_data", Imu, queue_size=2)
    rospy.init_node("imu_publisher")
    rate = rospy.Rate(400)
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
    calibratedDataX = []
    calibratedDataY = []
    for i in range(400):
        zenEvent = client.wait_for_next_event()

        # check if its an IMU sample event and if it
        # comes from our IMU and sensor component
        if zenEvent.event_type == openzen.ZenEventType.ImuData and \
            zenEvent.sensor == imu.sensor and \
            zenEvent.component.handle == imu.component.handle:

            imu_data = zenEvent.data.imu_data
        acc_init = np.array(imu_data.a)
        calibratedData.append(acc_init)
        calibratedDataX.append(acc_init[0])
        calibratedDataY.append(acc_init[1])
        i+=1

    x_offset = sum(calibratedDataX)/len(calibratedDataX)
    y_offset = sum(calibratedDataY)/len(calibratedData)
    np_calibratedData = np.array(calibratedData)
    g = np.sum(np.linalg.norm(np_calibratedData, axis=1)/np.shape(np_calibratedData)[0])
    #     print("Calibration Completed")
    # start streaming data

    dir = os.path.dirname(os.path.realpath(__file__))[:-7] 
    M = np.load(dir + 'data' + '/sensitivity.npy')
    b_a = np.load(dir + 'data' + '/offset.npy')
    Mi = np.linalg.inv(M)
    b_i =[0.96221395, -0.96221395]
    a_i =[0.9244278933486572]
    r_acc_1 = np.zeros(3)
    r_acc_filt_1 = np.zeros(3)

    t_prev = rospy.get_time()
    while not rospy.is_shutdown():
        try:
            
            zenEvent = client.wait_for_next_event()

            # check if its an IMU sample event and if it
            # comes from our IMU and sensor component
            if zenEvent.event_type == openzen.ZenEventType.ImuData and \
                zenEvent.sensor == imu.sensor and \
                zenEvent.component.handle == imu.component.handle:

                imu_data = zenEvent.data.imu_data
            acc = np.array(imu_data.a) #- np.array([x_offset, y_offset, 0])
            #print(calibratedDataX, calibratedDataY)
            #acc_r = acc.reshape(3,1)
            #diff =  (acc_r - b_a)
            #acc_hat = np.dot(Mi,diff)
            #print(acc_hat)
            #print(acc_hat)
            #acc_hat = acc_hat.reshape(3)
            #print(acc_hat)
            #acc_hat = np.asarray(acc_hat)
            quat = np.array(imu_data.q)
            r = R.from_quat([-quat[1],-quat[2],-quat[3],quat[0]])
            r_acc = r.apply(acc)
            r_acc = (r_acc + np.array([0, 0, g]))*9.81
            print(r_acc)
            r_acc_filt = a_i[0]*r_acc_filt_1 + b_i[0]*r_acc + b_i[1]*r_acc_1
            
            time = rospy.get_time()
            imu_raw.dt = time - t_prev
            imu_raw.acceleration.x = r_acc[0]
            imu_raw.acceleration.y = r_acc[1]
            imu_raw.acceleration.z = r_acc[2]
            imu_raw.linearaccel.x = r_acc_filt[0]
            imu_raw.linearaccel.y = r_acc_filt[1]
            imu_raw.linearaccel.z = r_acc_filt[2]
            imu_raw.orientation.w = quat[0]
            imu_raw.orientation.x = -quat[1]
            imu_raw.orientation.y = -quat[2]
            imu_raw.orientation.z = -quat[3]
            
            #print(acc)
            #imu_raw.stamp = rospy.Time.now()
            imuPub.publish(imu_raw)
            r_acc_1 = r_acc
            r_acc_filt_1 = r_acc_filt
            t_prev = time
        except rospy.ROSInterruptException:
            pass
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass