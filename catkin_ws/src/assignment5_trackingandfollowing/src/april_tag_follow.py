#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist, Point
from geometry_msgs.msg  import PoseWithCovariance
from turtlesim.msg import Pose
import numpy as np
from apriltag_ros.msg import AprilTagDetectionArray

#x = 0
#z = 0



def callback(msg):
        #global x,z
		# if not msg:
		# 	pos  = 0
		# else:
        #x = msg.detections[0].pose.pose.pose.position.x

        #print ('X is', x )
	try:
		x = msg.detections[0].pose.pose.pose.position.x
		z = msg.detections[0].pose.pose.pose.position.z
            #print ('Position is', x )
	    #print('Depth is', z)
		move.linear.x = z*5
		move.angular.z = -x*75
		pub.publish(move)
            
	except IndexError:
            #print('Out of index,,,yoooo')
		x = 0 
		z = 0
		move.linear.x = z*5
		move.angular.z = x*50
		pub.publish(move)
            
 #    	head = msg.ranges[1:50]
 #    	tail = msg.ranges[300:359]
 #    	distances.extend(head)
 #    	distances.extend(tail)
 #    	dist = max(distances)
	# print("The min distance is " + str(dist))
	
# rate = rospy.Rate(10)   
move = Twist()
rospy.init_node('vel_scan', anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
# rate = rospy.Rate(10)
subscriber = rospy.Subscriber('/tag_detections', AprilTagDetectionArray, callback)
rospy.spin()
    # pose = Pose()
    #rate = rospy.Rate(10)
    #move = Twist()
    #print('X and Z are', x,z)
    #move.linear.x = z*5
    #move.angular.z = x*50
    
    
 #    stop_dist = 0.5
    #while dist > stop_dist:
        #move.linear.x = 0.2
  #pub.publish(move)
#	rate.sleep()
	
 #    move.linear.x = 0
    #pub.publish(move)
    #rospy.spin()
#if __name__ == '__main__':
 #   try:
  #      x = turtlebot()
   # except rospy.ROSInterruptException: pass
