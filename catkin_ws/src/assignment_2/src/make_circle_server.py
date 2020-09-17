#!/usr/bin/env python

import rospy
from assignment_2.srv import MakeCircle
from geometry_msgs.msg import Twist

def process_make_circle(req):
	pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
	vel_msg = Twist()
	radius = req.r
	speed = req.s

	vel_msg.linear.x = speed
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = speed/radius

	while not rospy.is_shutdown():
		pub.publish(vel_msg)

	vel_msg.linear.x = 0
	vel_msg.angular.z = 0
	pub.publish(vel_msg)


def move_circle():
	rospy.init_node('move_circle_server')
	service = rospy.Service('move_circle',MakeCircle,process_make_circle)
	rospy.spin()

if __name__ == '__main__':
		move_circle()	

