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

# Your serial port might be different!

def runLoop():
    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    b = TransformBroadcaster()
    #marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
    translation = (0.0, 0.0, 0.0)
    rotation = (0.0, 0.0, 0.0, 1.0)
    rate = rospy.Rate(100) # 

    calibratedData = []
    rawDataList = []
    calibratedDataList = []
    vel = [0, 0 , 0]
    dist = [0, 0, 0]
    rawDataList = []

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

            # r_acc = r_acc - np.array([0, 0, 9.81])
            # for i in range(len(r_acc)):
            #     if abs(r_acc[i]) < 0.5:
            #         r_acc[i] = 0
                
            # for i in range(len(r_acc)):
            #     if (r_acc[i]) == 0:
            #         vel[i] = 0
    
            vel = vel + r_acc*dt
            dist = (dist + vel*dt)
        
        
            translation=(dist[0], dist[1], dist[2])
            rotation = (quat[1], quat[2], quat[3], quat[0])
            rospy.loginfo(np.linalg.norm(r_acc))



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