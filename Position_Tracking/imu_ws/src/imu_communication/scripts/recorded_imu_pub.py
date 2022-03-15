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
import csv


def getData(file):
    """
    Reads the data from the recorded lpms data file 
    and retuns the time stamp(s), acceleration(g), 
    & quaternion (W,X,Y,Z) as a list of lists
    """
    with open(file, "r") as i:
        rawdata = list(csv.reader(i,delimiter=","))
    header = rawdata[0]
    data = np.array(rawdata[1:],dtype=float)
    t_stamp = data[:,1]
    acc =  data[:,3:6]
    quat = data[:,15:19]
    lin_acc = data[:,20:23]
    return t_stamp, acc, quat


def main():
    t_stamp, acc, quat = getData(file)
    imuPub = rospy.Publisher("/recorded_imu_data", Imu, queue_size=2)
    rospy.init_node("recorded_imu_publisher")
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

    calibratedData = []
    for i in range(400):
            acc_init = acc[i]
            quat_init = quat[i]
            print(quat_init[0])
            calibratedData.append(acc_init)
            i+=1

    np_calibratedData = np.array(calibratedData)
    g = np.sum(np.linalg.norm(np_calibratedData, axis=1)/np.shape(np_calibratedData)[0])
    print(g)

    t_i_1 = 0
    for i in range(len(acc)):
        try:
            acc_i = acc[i]
            quat_i = quat[i]
            r = R.from_quat([-quat_i[1],-quat_i[2],-quat_i[3],quat_i[0]])
            r_acc = r.apply(acc_i)
            r_acc = (r_acc + np.array([0, 0, g]))*9.81
            #r_acc_filt = a_i[0]*r_acc_filt_1 + b_i[0]*r_acc + b_i[1]*r_acc_1
            imu_raw.dt = t_stamp[i] - t_i_1
            print(imu_raw.dt)
            imu_raw.acceleration.x = r_acc[0]
            imu_raw.acceleration.y = r_acc[1]
            imu_raw.acceleration.z = r_acc[2]
            # imu_raw.linearaccel.x = r_acc_filt[0]
            # imu_raw.linearaccel.y = r_acc_filt[1]
            # imu_raw.linearaccel.z = r_acc_filt[2]
            imu_raw.orientation.w = quat_i[0]
            imu_raw.orientation.x = -quat_i[1]
            imu_raw.orientation.y = -quat_i[2]
            imu_raw.orientation.z = -quat_i[3]
            
            imuPub.publish(imu_raw)
            #r_acc_1 = r_acc
            #r_acc_filt_1 = r_acc_filt
            t_i_1 = t_stamp[i]
        except rospy.ROSInterruptException:
            pass
        rate.sleep()



if __name__ == "__main__":
    #try:
    dir = os.path.dirname(os.path.realpath(__file__))[:-7]
    file = dir  + "data" + "/lpmsdata2.csv"
    main()
    #except:
    print("Please enter a correct file name")