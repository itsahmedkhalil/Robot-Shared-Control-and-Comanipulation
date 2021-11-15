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
    damp = 1    
    r_acc_last = [0, 0, 0]

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


    #w = tk.Tk()
    print("Calibration Started")
    for i in range(200):
         ser_bytes = ser.readline() 
         decoded_bytes = str(ser_bytes.decode("ascii"))
         if decoded_bytes[0] != 'C':
            rawData = [float(x) for x in decoded_bytes.split(",")]
            #rawDataList.append(rawData)
            acc_init = np.array(rawData[0:3])
            quat_init = rawData[3:]
            r_init = R.from_quat([quat_init[1], quat_init[2], quat_init[3], quat_init[0]])
            cal_acc = r_init.apply(acc_init)
            calibratedData.append(cal_acc)
            i+=1
         pass
    np_calibratedData = np.array(calibratedData)
    #gravityDF = pd.DataFrame(calibratedData, columns =['accx','accy','accz']) 
    #print(gravityDF)
    #g = np.sum((gravityDF['accX']**2 + gravityDF['accY']**2 +gravityDF['accZ']**2)**0.5)/np.size(gravityDF['accz'])
    g = np.sum(np.linalg.norm(np_calibratedData, axis=1)/np.shape(np_calibratedData)[0])
    print("Gravity: ", g)
    print("Calibration Finished")
    vel = np.zeros(3)
    dist = np.zeros(3)  
    #dt = 0.01 #need to be changed from Arduino
    print("Calibrated")
    counter = 0
    x_n = 0
    x_n_1 = 0
    x_n_2 = 0
    t_old = float(time())
    data_list = []
    while not rospy.is_shutdown():
        try:
            t = float(time())
            #print(t)
            ser_bytes = ser.readline()  
            decoded_bytes = str(ser_bytes.decode("ascii"))
            if decoded_bytes[0] != 'C':
                rawData = [float(x) for x in decoded_bytes.split(",")]
                acc = np.array(rawData[0:3])
                quat = rawData[3:]
            
            r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
            r_acc = r.apply(acc)
            
            r_acc = r_acc - np.array([0, 0, g])
            
            dt = t - t_old

            for i in range(len(r_acc)):
                x_n = (2*x_n_1 - x_n_2 + damp*x_n_1*dt+r_acc*dt*dt)/(damp*dt+1)

            
            
            # vel = vel + r_acc*dt
            # dist = (dist + vel*dt)
            # r_acc_last = r_acc
            print(np.linalg.norm(r_acc))
            #print(x_n[0], x_n[1], x_n[2])
            translation=(x_n[0], x_n[1], x_n[2])
            rotation = (quat[1], quat[2], quat[3], quat[0])


            #marker distance between imu and marker
            delta_distX = abs(dist[0] - marker.pose.position.x)
            delta_distY = abs(dist[1] - marker.pose.position.y)
            
            #if the distance is cloes to 0, the marker move to a random position
            if delta_distX < 0.05 and delta_distY < 0.05:
                counter += 1
                marker.pose.position.x = float(random.randint(-10, 10))/10
                marker.pose.position.y = float(random.randint(-10,10))/10
                print("new marker position:", marker.pose.position.x, marker.pose.position.y)
                marker.pose.position.z = 0
                print("you got number of points! :", counter)

            else:
                pass
            marker_pub.publish(marker)
            #rospy.loginfo(np.linalg.norm(r_acc))
            b.sendTransform(translation, rotation, Time.now(), 'arduino', '/world')
            #rospy.loginfo(marker)
            t_old = t
            x_n_2 = x_n_1
            x_n_1 = x_n
        except Exception as e:
            #t = float(time())
            #print(e)
            pass
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('my_broadcaster')
    runLoop()
    rospy.spin