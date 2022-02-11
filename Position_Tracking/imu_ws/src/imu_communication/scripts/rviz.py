#!/usr/bin/env python
# license removed for brevity
from unicodedata import name
import rospy
from imu_communication.msg import Imu
from visualization_msgs.msg import Marker
from time import time
import tf2_ros
from tf import TransformBroadcaster
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import random
import sys

class imu_visualizer:
    def __init__(self):
        self.t_prev = rospy.get_time()
        self.sub = rospy.Subscriber("/imu_data", Imu, self.callback)
        self.marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
        self.marker = Marker()
        self.marker.header.frame_id = "world"
        self.marker.pose.orientation.x = 0.0
        self.marker.pose.orientation.y = 0.0
        self.marker.pose.orientation.z = 0.0
        self.marker.pose.orientation.w = 1.0

        #marker initial position
        self.marker.pose.position.x = 0
        self.marker.pose.position.y = 0
        self.marker.pose.position.z = 0

        # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
        self.marker.type = 1
        self.marker.id = 0
        # Set the scale of the marker
        self.marker.scale.x = 0.05
        self.marker.scale.y = 0.05
        self.marker.scale.z = 0.05
        # Set the color
        self.marker.color.r = 0.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.0
        self.marker.color.a = 1.0
        self.counter = 0
        
        self.imu = Imu()
        self.quat = np.array([0, 0, 0, 1])
        self.acc = np.array([0, 0, 0])
        self.damp = np.array([0.01, 0.01, 0.01])
        self.vel = np.array([0, 0, 0])
        self.x_n = np.array([0, 0, 0])
        self.x_n_1 = np.array([0,0,0])
        self.t_prev = rospy.get_time()
        self.br = tf2_ros.TransformBroadcaster()
        self.translation = (0.0, 0.0, 0.0)
        self.rotation = (0.0, 0.0, 0.0, 1.0)
        
    def callback(self, data):
        self.acc = np.array([data.linearaccel.x, data.linearaccel.y, data.linearaccel.z])
        self.quat = np.array([data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]) 
        self.t = data.time   
        dt = (self.t - self.t_prev)
        f = 1/dt
        self.vel = (self.vel + self.acc*dt)/(1+self.damp*dt)
        self.t_prev = self.t
        self.x_n = self.x_n_1 + dt*self.vel
        self.x_n_1 = self.x_n

        self.translation=(self.x_n[0], self.x_n[1], 0)
        self.rotation = (self.quat[1], self.quat[2], self.quat[3], -self.quat[0])
        self.br.sendTransform(self.translation, self.rotation, Time.now(), 'imu', '/world')
        delta_distX = abs(self.x_n[0] - self.marker.pose.position.x)
        delta_distY = abs(self.x_n[1] - self.marker.pose.position.y)
        #if the distance is cloes to 0, the marker move to a random position
        if delta_distX < 0.05 and delta_distY < 0.05:
            self.counter += 1
            self.marker.pose.position.x = float(random.randint(-5, 5))/20
            self.marker.pose.position.y = float(random.randint(-5,5))/20
            print("new marker position:", self.marker.pose.position.x, self.marker.pose.position.y)
            self.marker.pose.position.z = 0
            print("you got number of points! :", self.counter)

        else:
            pass
        self.marker_pub.publish(self.marker)
        
if __name__ == '__main__':
    try:
        rospy.init_node('imu_publisher', anonymous=True)
        a = imu_visualizer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass