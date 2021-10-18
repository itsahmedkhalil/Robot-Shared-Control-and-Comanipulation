#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import Float64
import serial
from imu_communication.msg import Num
from visualization_msgs.msg import Marker

# Your serial port might be different!




def runLoop():
    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    rospy.init_node('rviz_marker')
    marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
    #state_pub = rospy.Publisher("answer",Num, queue_size=20)
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    marker = Marker()
    marker.header.frame_id = "base_link"
    #marker.pose.position.x = 0
    #marker.pose.position.y = 0
    #marker.pose.position.z = 0
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
    marker.type = 1
    marker.id = 0

    # Set the scale of the marker
    marker.scale.x = 1.0
    marker.scale.y = 1.0
    marker.scale.z = 1.0

    # Set the color
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    #msg_to_publish = Num()
    while not rospy.is_shutdown():
        try:
            ser_bytes = ser.readline()  
            decoded_bytes = str(ser_bytes.decode("ascii"))
            rows = [float(x) for x in decoded_bytes.split(",")]
            if len(rows) == 9:      
                marker.pose.position.x = rows[0]
                marker.pose.position.y = rows[1]
                marker.pose.position.z = 0
                marker.pose.orientation.x = 0.0
                marker.pose.orientation.y = 0.0
                marker.pose.orientation.z = 0.0
                marker.pose.orientation.w = 1.0
                marker.header.stamp = rospy.Time.now()
                #msg_to_publish.accX = rows[0]
                #msg_to_publish.accY = rows[1]
                #if decoded_bytes==1 or decoded_bytes==0:
                #state_pub.publish(msg_to_publish)
                #rospy.loginfo(msg_to_publish)
                marker_pub.publish(marker)
                rospy.loginfo(marker.pose.position.y)
                rospy.rostime.wallsleep(1.0)
            #print(accx)
        
        except Exception as e:
            print("not Working")
            pass
        rate.sleep()

if __name__ == '__main__':
    try:
        runLoop()
    except rospy.ROSInterruptException:
        pass