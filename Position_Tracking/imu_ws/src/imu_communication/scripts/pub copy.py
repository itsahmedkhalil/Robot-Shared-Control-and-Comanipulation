#!/usr/bin/env python
# license removed for brevity
from pickle import TRUE
import rospy
from std_msgs.msg import Float64
import serial
from imu_communication.msg import Num
from visualization_msgs.msg import Marker

from time import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class positionTracking:

    def __init__(self):
        self.ser = serial.Serial('/dev/arduinoNano', timeout=1)  #Change serial port
        self.pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
        self.rate = rospy.Rate(10) # 10hz
        self.calibrate = False
        self.dt = 0.025
        self.marker = Marker()
        self.marker.header.frame_id = "base_link"
        self.marker.pose.orientation.x = 0.0
        self.marker.pose.orientation.y = 0.0
        self.marker.pose.orientation.z = 0.0
        self.marker.pose.orientation.w = 1.0
        # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
        self.marker.type = 1
        self.marker.id = 0

        # Set the scale of the marker
        self.marker.scale.x = 0.1
        self.marker.scale.y = 0.1
        self.marker.scale.z = 0.1

        # Set the color
        self.marker.color.r = 0.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.0
        self.marker.color.a = 1.0
         

    def calibrate(self):
        if self.calibrate == True:
            pass
        else:
            rawDataList = []
            for i in range(100):
                ser_bytes = self.ser.readline()  
                decoded_bytes = str(ser_bytes.decode("ascii"))
                rawData = [float(x) for x in decoded_bytes.split(",")]
                rawDataList.append(rawData)
                i+=1
            rawDataDF = pd.DataFrame(rawDataList, columns =['accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz']) 
            self.noise_acc = [np.sum(rawDataDF['accx'])/np.size(rawDataDF['accx']),np.sum(rawDataDF['accy'])/np.size(rawDataDF['accy']),np.sum(rawDataDF['accz'])/np.size(rawDataDF['accz'])]
            self.vel = np.zeros(3)
            self.dist = np.zeros(3)              
            self.calibrate = True

    def positionTracking(self):
        ser_bytes = self.ser.readline()  
        decoded_bytes = str(ser_bytes.decode("ascii"))
        rawData = [float(x) for x in decoded_bytes.split(",")]
        acc = rawData[0:3] - self.noise_acc
        for i in range(len(acc)):
            if abs(acc[i]) < 0.05:
                acc[0] = 0
        for i in range(len(acc)):
            if (acc[i]) == 0    :
                self.vel[i] = self.vel[i] * 0.25
        self.vel = self.vel + acc*self.dt
        self.dist = (self.dist + self.vel*self.dt)
        # print(np.sum(rawDataDF['accz']),np.size(rawDataDF['accz']), noise_accz)
        self.marker.pose.position.x = self.dist[0]
        self.marker.pose.position.y = self.dist[1]
        self.marker.pose.position.z = 0
        self.marker.pose.orientation.x = 0.0
        self.marker.pose.orientation.y = 0.0
        self.marker.pose.orientation.z = 0.0
        self.marker.pose.orientation.w = 1.0
        self.marker.header.stamp = rospy.Time.now()
        #msg_to_publish.accX = rows[0]
        #msg_to_publish.accY = rows[1]
        #if decoded_bytes==1 or decoded_bytes==0:
        #state_pub.publish(msg_to_publish)
        #rospy.loginfo(msg_to_publish)
        self.pub.publish(self.marker)
        rospy.loginfo(self.marker)



if __name__ == '__main__':
    rospy.init_node('rviz_marker')
    positionTracking()
    rospy.spin