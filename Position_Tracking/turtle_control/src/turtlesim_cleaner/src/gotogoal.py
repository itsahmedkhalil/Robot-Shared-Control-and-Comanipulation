#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
from std_msgs.msg import Float64
import serial
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


class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(100)

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)


    def move2goal(self):
        ser = serial.Serial('/dev/ttyACM0', timeout=1)
        rate = rospy.Rate(100) # 

        rawDataList = []
        vel = [0, 0 , 0]
        dist = [0, 0, 0]
        rawDataList = []
        goal_pose = Pose()
        vel_msg = Twist()

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
                    gyro = rawData[3:6]
                r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
                r_acc = r.apply(acc)

                r_acc = r_acc - np.array([0, 0, 9.81])
                # for i in range(len(r_acc)):
                #     if abs(r_acc[i]) < 0.5:
                #         r_acc[i] = 0
                    
                # for i in range(len(r_acc)):
                #     if (r_acc[i]) == 0:
                #         vel[i] = 0
        
                vel = vel + r_acc*dt
                dist = (dist + vel*dt)
        
                
                goal_pose.x = dist[0]
                goal_pose.y = dist[1]

                vel_msg.linear.x = vel[0]
                vel_msg.linear.y = vel[1]
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = 0

                # Publishing our vel_msg
                self.velocity_publisher.publish(vel_msg)
                rospy.loginfo(dist[])


            except Exception as e:
                print(e)
                pass
            rate.sleep()
        

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass