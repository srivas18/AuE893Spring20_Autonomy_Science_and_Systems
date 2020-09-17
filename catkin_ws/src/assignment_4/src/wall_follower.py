#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist, Point
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
from sensor_msgs.msg import LaserScan
import numpy as np
import sys

dist_side = 0
dist_front = 0
#global dist


def callback(msg):

    global dist_side
    global dist_front
    e01 = 0.0; e11 = 0; e21 = 0   
    u1 = 0;
    kp1= 0.4; ki1=0; kd1= .250 # Defining PID parameters   
    k11 = kp1+ ki1+ kd1
    k21 = -kp1-2*kd1
    k31 = kd1
    distances = []  
    distances_front = []
    head1 = msg.ranges[1:9]
    head2 = msg.ranges[351:359]
    tail = msg.ranges[270:320]
    distances_front.extend(head1)
    distances_front.extend(head2)
    distances.extend(tail)

    dist_front = sum(distances_front)/(len(distances_front))

    left_region =  msg.ranges[30:90]

    left_region = sort(left_region)
    left_dist =  sum(left_region)/(len(left_region))


    right_region = msg.ranges[270:330]
    right_region = sort(right_region)
    right_dist = sum(right_region)/(len(right_region))

    if dist_front > 10:
        dist_front = 10


    move = Twist()

    wall_dist = 1
    vel = 0.5


    z = 1
    e = 0
    error = left_dist - right_dist
    print('Error', error)
    error_front = 1.4 - dist_front
    print('Error front', error_front)
    if error_front < 0:
        print('Condition 1')
        move.linear.x = vel
        e21 = e11
        e11 = e01
        e01 = error
        u1 =  u1 + k11*e01 + k21*e11 + k31*e21
        print(u1)
        move.angular.z = u1
        pub.publish(move)
    else:
        print('Condition 2')
        move.linear.x = vel - 0.25
        move.angular.z = 1.5*(error_front + error) 
        pub.publish(move) 

def sort (unsorted_list):
    sorted_list = []
    for i in unsorted_list:
        if i > 1000:
            pass
        else:
            sorted_list.append(i)
    return sorted_list        



move = Twist() # Creates a Twist message type object
rospy.init_node('vel_scan') # Initializes a node
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  # Publisher object which will publish "Twist" type messages
                                             # on the "/cmd_vel" Topic, "queue_size" is the size of the
                                                         # outgoing message queue used for asynchronous publishing

sub = rospy.Subscriber("/scan", LaserScan, callback)  # Subscriber object which will listen "LaserScan" type messages
                                                      # from the "/scan" Topic and call the "callback" function
                              # each time it reads something from the Topic

# pub.publish(move)                             

rospy.spin()

