#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import numpy as np
from slerp.msg import Input
from geometry_msgs.msg import Quaternion
import time

def input_and_send():
    q1 = list(input("Enter the first quaternion values with commas seperating (ex.1,2,3,4):").replace(",",""))
    q2 = list(input("Enter the second quaternion values with commas seperating (ex.1,2,3,4):").replace(",",""))
    t = float(input("Enter the interpolation number 0<t<1:"))
    q1 = np.array([float(i) for i in q1])
    q2 = np.array([float(i) for i in q2])

    rospy.Subscriber("send_answer", String, callback)

    pub = rospy.Publisher('send_input', Input, queue_size=10)
    rospy.init_node('communicator', anonymous=True)
    msg = Input()
    msg.q1 = Quaternion(*q1)
    msg.q2 = Quaternion(*q2)
    msg.t = t
    pub.publish(msg)

    rospy.spin()

def callback(data):
    rospy.loginfo("Answer: %s", data.data)

if __name__ == '__main__':
    try:
        input_and_send()
    except rospy.ROSInterruptException:
        pass

