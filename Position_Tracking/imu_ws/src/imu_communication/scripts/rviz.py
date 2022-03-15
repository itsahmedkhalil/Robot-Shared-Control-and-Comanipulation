#!/usr/bin/env python
# license removed for brevity
from unicodedata import name
import rospy
from imu_communication.msg import Imu
from visualization_msgs.msg import Marker
from time import time
import tf2_ros
from geometry_msgs.msg import TransformStamped
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import random
import sys

class imu_visualizer:
    def __init__(self):
        self.t_prev = rospy.get_time()
        self.rate = rospy.Rate(400)
        self.sub = rospy.Subscriber("/imu_data", Imu, self.callback)
        self.marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 1)
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
        self.marker.scale.x = 0.1
        self.marker.scale.y = 0.1
        self.marker.scale.z = 0.1
        # Set the color
        self.marker.color.r = 0.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.0
        self.marker.color.a = 1.0
        self.counter = 0
        
        self.imu = Imu()
        self.damp = np.array([0.0, 0.0, 0.0])
        self.vel = np.zeros(3)
        self.x_n = np.zeros(3)
        self.x_n_1 = np.zeros(3)
        self.t_prev = rospy.get_time()
        self.br = tf2_ros.TransformBroadcaster()
        self.tr = TransformStamped()
        self.tr.transform.translation.x = 0
        self.tr.transform.translation.y = 0
        self.tr.transform.translation.z = 0
        self.tr.transform.rotation.x = 0
        self.tr.transform.rotation.y = 0
        self.tr.transform.rotation.z = 0
        self.tr.transform.rotation.w = 1
        
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
        self.tr.header.stamp = Time.now()
        self.tr.header.frame_id = "world"
        self.tr.child_frame_id = "imu"
        self.tr.transform.translation.x = self.x_n[0]
        self.tr.transform.translation.y = self.x_n[1]
        self.tr.transform.translation.z = self.x_n[2]
        self.tr.transform.rotation.x = quat[0]
        self.tr.transform.rotation.y = quat[1]
        self.tr.transform.rotation.z = quat[2]
        self.tr.transform.rotation.w = quat[3]
        self.br.sendTransform(self.tr)
        delta_distX = abs(self.x_n[0] - self.marker.pose.position.x)
        delta_distY = abs(self.x_n[1] - self.marker.pose.position.y)
        #if the distance is cloes to 0, the marker move to a random position
        if delta_distX < 0.05 and delta_distY < 0.05:
            self.counter += 1
            self.marker.pose.position.x = float(random.randint(-5, 5))/20
            self.marker.pose.position.y = float(random.randint(-5, 5))/20
            print("new marker position:", self.marker.pose.position.x, self.marker.pose.position.y)
            self.marker.pose.position.z = 0
            print("you got number of points! :", self.counter)

        else:
            pass
        self.x_n_1 = self.x_n
        self.marker_pub.publish(self.marker)
        self.rate.sleep()
        
if __name__ == '__main__':
    try:
        rospy.init_node('rviz_broadcast', anonymous=True)
        a = imu_visualizer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass