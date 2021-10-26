#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64
import serial
from imu_communication.msg import Num
from visualization_msgs.msg import Marker
from time import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Your serial port might be different!

def runLoop():
    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
    rate = rospy.Rate(100) # 10hz
    marker = Marker()
    marker.header.frame_id = "base_link"
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
    marker.type = 1
    marker.id = 0
    # Set the scale of the marker
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1
    # Set the color
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    calibratedData = []
    rawDataList = []
    calibratedDataList = []
    vel = [0, 0 , 0]
    dist = [0, 0, 0]
    rawDataList = []

    print("Calibration Started")
    for i in range(100):
        ser_bytes = ser.readline()  
        decoded_bytes = str(ser_bytes.decode("ascii"))
        rawData = [float(x) for x in decoded_bytes.split(",")]
        rawDataList.append(rawData)
        i+=1
    rawDataDF = pd.DataFrame(rawDataList, columns =['accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz']) 
    noise_acc = [np.sum(rawDataDF['accx'])/np.size(rawDataDF['accx']),np.sum(rawDataDF['accy'])/np.size(rawDataDF['accy']),np.sum(rawDataDF['accz'])/np.size(rawDataDF['accz'])]
    vel = np.zeros(3)
    dist = np.zeros(3)  
    dt = 0.025
    print("Calibrated")
    
    while not rospy.is_shutdown():
        try:
            t = float(time())
            ser_bytes = ser.readline()  
            decoded_bytes = str(ser_bytes.decode("ascii"))
            rawData = [float(x) for x in decoded_bytes.split(",")]
            acc = np.subtract(rawData[0:3], noise_acc)
            for i in range(len(acc)):
                if abs(acc[i]) < 0.005:
                    acc[0] = 0
            # for i in range(len(acc)):
            #     if (acc[i]) == 0    :
            #         vel[i] = 0
            vel = vel + acc*dt
            dist = (dist + vel*dt)
            marker.pose.position.x = dist[0]
            marker.pose.position.y = dist[1]
            marker.pose.position.z = 0
            marker.pose.orientation.x = 0.0
            marker.pose.orientation.y = 0.0
            marker.pose.orientation.z = 0.0
            marker.pose.orientation.w = 1.0
            marker.header.stamp = rospy.Time.now()
            marker_pub.publish(marker)
            #rospy.loginfo(marker)
            #print(acc)
            #print(1/(time() - t))
        except Exception as e:
            print("not Working")
            pass
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('rviz_marker')
    runLoop()
    rospy.spin