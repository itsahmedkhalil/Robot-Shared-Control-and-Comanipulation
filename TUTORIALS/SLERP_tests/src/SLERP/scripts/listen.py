#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from SLERP.msg import Num
import numpy as np
import quaternion


publisher = rospy.Publisher("answer",String, queue_size=20)
def callback(data):
    q1 = np.quaternion(data.q1.x, data.q1.y,data.q1.z,data.q1.w)
    q2 = np.quaternion(data.q2.x, data.q2.y,data.q2.z,data.q2.w)
    answer = str(quaternion.slerp_evaluate(q1,q2,data.t))
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        publisher.publish(answer)
        rospy.loginfo("answer went through")
        r.sleep()

def listen():
   
   rospy.init_node('listen', anonymous=True)
   
   rospy.Subscriber("input", Num, callback)
    
   rospy.spin()

if __name__ == '__main__':
    listen()
