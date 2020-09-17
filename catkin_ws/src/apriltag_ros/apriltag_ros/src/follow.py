#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist, Point
from geometry_msgs.msg  import PoseWithCovariance
from turtlesim.msg import Pose
import numpy as np

pos = 10000

class turtlebot():

    def callback(msg):
        global pos
		# if not msg:
		# 	pos  = 0
		# else:
        x = msg
        print ('X is', X )
 #    	head = msg.ranges[1:50]
 #    	tail = msg.ranges[300:359]
 #    	distances.extend(head)
 #    	distances.extend(tail)
 #    	dist = max(distances)
	# print("The min distance is " + str(dist))
	
    
    rospy.init_node('vel_scan', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    pose_subscriber = rospy.Subscriber('/tag_detections', PoseWithCovariance, callback)
    # pose = Pose()
 #    rate = rospy.Rate(10)
 #    move = Twist()
    
 #    stop_dist = 0.5
 #    while dist > stop_dist:
	# move.linear.x = 0.2
	# pub.publish(move)
	# rate.sleep()
	
 #    move.linear.x = 0
 #    pub.publish(move)
    rospy.spin()
if __name__ == '__main__':
    try:
        x = turtlebot()
    except rospy.ROSInterruptException: pass
