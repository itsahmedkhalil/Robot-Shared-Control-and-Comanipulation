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
import sys
np.set_printoptions(threshold=sys.maxsize)

# Your serial port might be different!




def runLoop():
    ser = serial.Serial('/dev/arduinoNano', timeout=1)
    rospy.init_node('rviz_marker')
    marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
    #state_pub = rospy.Publisher("answer",Num, queue_size=20)
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    marker = Marker()
    marker.header.frame_id = "base_link"
    #marker.pose.position.x = 0
    #marker.pose.position.y = 0
    #marker.pose.position.z = 0
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
    t_0 = float(time()) #Time when code is first run
    noise_accx = 0  #Dummy variable for accelerometer noise in x axes
    noise_accy = 0  #Dummy variable for accelerometer noise in y axes
    noise_accz = 0  #Dummy variable for accelerometer noise in z axes

    rowlist = []
    calibratedData = []
    rawDataList = []
    calibratedDataList = []
    vel = [0, 0 , 0]
    dist = [0, 0, 0]

    #msg_to_publish = Num()
    while not rospy.is_shutdown():
        try:
            ser_bytes = ser.readline()  
            decoded_bytes = str(ser_bytes.decode("ascii"))
            rawData = [float(x) for x in decoded_bytes.split(",")]
            if len(rawData) == 9:      
                t_from_start = round(float(time()) - t_0,3) #Time from when the code when initally run
                rawData.insert(0, t_from_start)   #Insert time for each respective point 
                #rowlist.append(rows)   #Append row to l
                calibratedData = rawData
                
                calibratedData[1] = rawData[1] - noise_accx
                calibratedData[2] = rawData[2] - noise_accy
                calibratedData[3] = rawData[3] - noise_accz

                #Method 2: Creating threshold to get rid of noise
                if abs(calibratedData[1])<0.05:
                    calibratedData[1] = 0
                if abs(calibratedData[2])<0.05:
                    calibratedData[2] = 0
                if abs(calibratedData[3])<0.05:
                    calibratedData[3] = 0
               
                #Converting raw data into a dataframe
                rawDataList.append(rawData)
                rawDataDF = pd.DataFrame(rawDataList, columns =['time', 'accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz']) 
                
                #Converting 'calibrating' data in a dataframe
                calibratedDataList.append(calibratedData)
                calibratedDataDF = pd.DataFrame(calibratedDataList, columns =['time', 'accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz']) 

                acc = np.array([calibratedData[1], calibratedData[2],calibratedData[3]])

                #Method 1: Subtracting off bias
                #This is to get rid of noise. To use you have to make sure that the IMU is stationary for ~10 seconds. 
                #The code will collect 100 data points, average them, and subtract that number from all 
                #incoming accelerometer data in each respective axes. 
                if np.size(rawDataDF['accx']) == 100:
                            noise_accx = np.sum(rawDataDF['accx'])/np.size(rawDataDF['accx'])
                            noise_accy = np.sum(rawDataDF['accy'])/np.size(rawDataDF['accy'])
                            noise_accz = np.sum(rawDataDF['accz'])/np.size(rawDataDF['accz'])
                            vel = [0, 0 , 0]
                            dist = [0, 0, 0]
                            print('CALIBRATION DONE!')
                else:
                    dt = 25/1000
                    if acc[0] == 0:
                        vel[0] = 0
                    if acc[1] == 0:
                        vel[1] = 0
                    if acc[2] == 0:
                        vel[2] = 0
                    vel = vel + acc*dt
                    dist = dist + vel*dt
                posX = dist[0]*9.81*100
                posY = dist[1]*9.81*100
                posZ = dist[2]*9.81*100

                # print(np.sum(rawDataDF['accz']),np.size(rawDataDF['accz']), noise_accz)
                marker.pose.position.x = posX
                marker.pose.position.y = posY
                marker.pose.position.z = 0
                marker.pose.orientation.x = 0.0
                marker.pose.orientation.y = 0.0
                marker.pose.orientation.z = 0.0
                marker.pose.orientation.w = 1.0
                marker.header.stamp = rospy.Time.now()
                #msg_to_publish.accX = rows[0]
                #msg_to_publish.accY = rows[1]
                #if decoded_bytes==1 or decoded_bytes==0:
                #state_pub.publish(msg_to_publish)
                #rospy.loginfo(msg_to_publish)
                marker_pub.publish(marker)
                rospy.loginfo(marker)
                # rospy.rostime.wallsleep(25/1000)
            #print(accx)
        
        except Exception as e:
            print("not Working")
            pass
        rate.sleep()

if __name__ == '__main__':
    try:
        runLoop()
    except rospy.ROSInterruptException:
        pass