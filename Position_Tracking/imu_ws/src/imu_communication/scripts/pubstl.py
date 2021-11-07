#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64
import serial
from imu_communication.msg import Num
from visualization_msgs.msg import Marker
from time import time
import tf_conversions
import tf2_ros
import geometry_msgs.msg
from tf import TransformBroadcaster
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import random

# Your serial port might be different!

def runLoop():
    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    b = TransformBroadcaster()
    translation = (0.0, 0.0, 0.0)
    rotation = (0.0, 0.0, 0.0, 1.0)
    rate = rospy.Rate(100) # 

    calibratedData = []
    rawDataList = []
    calibratedDataList = []
    vel = [0, 0 , 0]
    dist = [0, 0, 0]
    rawDataList = []

    # Initialize the publisher for the marker
    marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
    marker = Marker()
    marker.header.frame_id = "world"
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    #marker initial position
    marker.pose.position.x = 0
    marker.pose.position.y = 0
    marker.pose.position.z = 0

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


    print("Calibration Started")
    # for i in range(100):
    #     ser_bytes = ser.readline() 
    #     decoded_bytes = str(ser_bytes.decode("ascii"))
    #     if decoded_bytes[0] != 'C':
    #         rawData = [float(x) for x in decoded_bytes.split(",")]
    #         rawDataList.append(rawData)
    #         i+=1
    #     pass
    # rawDataDF = pd.DataFrame(rawDataList, columns =['accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz', 'qW', 'qX', 'qY', 'qZ']) 
    # noise_acc = [np.sum(rawDataDF['accx'])/np.size(rawDataDF['accx']),np.sum(rawDataDF['accy'])/np.size(rawDataDF['accy']),np.sum(rawDataDF['accz'])/np.size(rawDataDF['accz'])]
    vel = np.zeros(3)
    dist = np.zeros(3)  
    dt = 0.01
    print("Calibrated")
    counter = 0
    while not rospy.is_shutdown():
        try:
            t = float(time())
            ser_bytes = ser.readline()  
            decoded_bytes = str(ser_bytes.decode("ascii"))
            if decoded_bytes[0] != 'C':
                rawData = [float(x) for x in decoded_bytes.split(",")]
                acc = np.array(rawData[0:3])
                quat = rawData[9:]
            
            r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
            r_acc = r.apply(acc)

            r_acc = r_acc - np.array([0, 0, 9.81])
            for i in range(len(r_acc)):
                if abs(r_acc[i]) < 0.1:
                    r_acc[i] = 0
                
            for i in range(len(r_acc)):
                if (r_acc[i]) == 0:
                    vel[i] = 0
    
            vel = vel + r_acc*dt
            dist = (dist + vel*dt)
        
        
            translation=(dist[0]*10, dist[1]*10, 0)
            rotation = (quat[1], quat[2], quat[3], quat[0])


            #marker distance between imu and marker
            delta_distX = dist[0] - marker.pose.position.x
            delta_distY = dist[1] - marker.pose.position.y
            
            #if the distance is cloes to 0, the marker move to a random position
            if 0<delta_distX < 0.1 and 0<delta_distY < 0.1:
                counter += 1
                marker.pose.position.x = random.randint(-2,2)
                marker.pose.position.y = random.randint(-2,2)
                print("new marker position:", marker.pose.position.x, marker.pose.position.y)
                marker.pose.position.z = 0
                print("you got number of points! :", counter)

            else:
                pass
            marker_pub.publish(marker)
            #rospy.loginfo(np.linalg.norm(r_acc))
            b.sendTransform(translation, rotation, Time.now(), 'arduino', '/world')
            #rospy.loginfo(marker)
            
        except Exception as e:
            print(e)
            pass
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('my_broadcaster')
    runLoop()
    rospy.spin