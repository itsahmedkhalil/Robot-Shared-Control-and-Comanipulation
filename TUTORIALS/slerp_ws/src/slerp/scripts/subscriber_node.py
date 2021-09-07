#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from slerp.msg import Input
import numpy as np
import quaternion
import time


def callback(data):
    pub = rospy.Publisher("send_answer", String, queue_size=1000)
    q1 = lambda o: np.array([o.x, o.y, o.z, o.w])
    q2 = lambda o: np.array([o.x, o.y, o.z, o.w])
    q1 = q1(data.q1)
    q2 = q2(data.q2) 
    q1 = np.quaternion(q1[0],q1[1],q1[2],q1[3])
    q2 = np.quaternion(q2[0],q2[1],q2[2],q2[3])
    t = data.t 
    ans = str(quaternion.as_float_array(quaternion.slerp_evaluate(q1, q2, t)))
    rospy.loginfo("Answer calculated")
    rospy.loginfo(ans)
    rospy.loginfo(type(ans))
    time.sleep(5)
    pub.publish(ans)
    time.sleep(5)
    rospy.loginfo("Answer sent")
   

def listener():
    rospy.init_node('calculator', anonymous=True)
    rospy.Subscriber('send_input', Input, callback)
    
    rospy.spin()

if __name__ == '__main__':
    listener()
