#!/usr/bin/env python

import rospy
from std_msgs import msg
from std_msgs.msg import String
from SLERP.msg import Num

def callback2(data):
    rospy.loginfo(data.data)

def slerper():
    pub = rospy.Publisher("input",Num, queue_size=20)
    rospy.init_node('slerper', anonymous=True)
    rate = rospy.Rate(10)


    while not rospy.is_shutdown():
        a, b, c, d = input("Enter first quaternion values with comma between (1,0,0,0):").replace(",","")
        w, x, y, z = input("Enter second quaternion values with comma between (0,1,0,0):").replace(",","") 
        t = float(input("Enter interpolation value between 0 and 1: "))
        msg_to_publish = Num()
        msg_to_publish.q1.x = float(a)
        msg_to_publish.q1.y = float(b)
        msg_to_publish.q1.z = float(c)
        msg_to_publish.q1.w = float(d)
        msg_to_publish.q2.x = float(w)
        msg_to_publish.q2.y = float(x)
        msg_to_publish.q2.z = float(y)
        msg_to_publish.q2.w = float(z)
        msg_to_publish.t = t
        pub.publish(msg_to_publish)
        rospy.Subscriber("answer", String, callback2)
        #rospy.spin()
        rate.sleep()


if __name__ == '__main__':
    try:
        slerper()
    except rospy.ROSInterruptException:
        pass