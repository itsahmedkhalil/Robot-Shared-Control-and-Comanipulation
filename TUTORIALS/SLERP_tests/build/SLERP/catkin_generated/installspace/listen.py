#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from SLERP.msg import Num
import numpy as np
import quaternion

def callback(data):
    answer = quaternion.slerp_evaluate(data.q1,data.q2,data.t)
    rospy.loginfo(answer)

def listen():
   
   rospy.init_node('listen', anonymous=True)
   
   rospy.Subscriber("function", Num, callback)
   print("hello")

   rospy.spin()
   
   if __name__ == '__main__':
       listen()
