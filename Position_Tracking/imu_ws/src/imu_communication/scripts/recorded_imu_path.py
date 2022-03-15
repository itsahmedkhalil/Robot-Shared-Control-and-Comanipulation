#!/usr/bin/env python
# license removed for brevity
from unicodedata import name
import rospy
from imu_communication.msg import Imu
from time import time
from geometry_msgs.msg import Pose, PoseStamped # Handles TransformStamped message
from nav_msgs.msg import Path
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import random
import sys

class ImuPath:
    def __init__(self):
        self.t_prev = rospy.get_time()
        self.rate = rospy.Rate(400)
        self.sub = rospy.Subscriber("/recorded_imu_data", Imu, self.callback)
        self.path_pub = rospy.Publisher("/path_maker",Path, queue_size =10)
        self.counter = 0        
        self.imu = Imu()
        self.path = Path()
        self.path.header.frame_id = "imu_frame"
        self.path.header.stamp = Time.now()
        self.damp = np.array([0.0, 0.0, 0.0])
        self.vel = np.zeros(3)
        self.x_n = np.zeros(3)
        self.x_n_1 = np.zeros(3)
        
    def callback(self, data):
        acc = np.array([data.acceleration.x, data.acceleration.y, data.acceleration.z])
        quat = np.array([data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]) 
        dt = data.dt
        self.vel = (self.vel + acc*dt)/(1+self.damp*dt)
        self.x_n = (self.x_n_1 + dt*self.vel)   
        if abs(acc[0]) < 0.0001:
            acc[0] = 0
            self.vel[0] = 0.0
        if abs(acc[1]) < 0.0001:
            acc[1] = 0
            self.vel[1] = 0.0
        if abs(acc[2]) < 0.0001:
            acc[2] = 0
            self.vel[2] = 0.0
        posestamp = PoseStamped()
        posestamp.header.stamp = Time.now()
        posestamp.header.frame_id = "imu_frame"
        #self.tr.child_frame_id = "imu"
        posestamp.pose.position.x = self.x_n[0]
        posestamp.pose.position.y = self.x_n[1]
        posestamp.pose.position.z = self.x_n[2]
        posestamp.pose.orientation.x = quat[0]
        posestamp.pose.orientation.y = quat[1]
        posestamp.pose.orientation.z = quat[2]
        posestamp.pose.orientation.w = quat[3]
        self.path.poses.append(posestamp)
        self.path_pub.publish(self.path)
        self.x_n_1 = self.x_n
        #self.rate.sleep()
        
if __name__ == '__main__':
    try:
        rospy.init_node('rviz_path_broadcast', anonymous=True)
        a = ImuPath()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass