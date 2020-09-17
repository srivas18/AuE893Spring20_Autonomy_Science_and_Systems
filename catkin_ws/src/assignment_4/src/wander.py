#!/usr/bin/env python
import rospy # Python library for ROS
from sensor_msgs.msg import LaserScan # LaserScan type message is defined in sensor_msgs
from geometry_msgs.msg import Twist #

angular_speed = 0.6
threshold = 1
angular_threshold = 0.5
    
def callback(data):

    front_region = []
    front_left = data.ranges[0:30]
    front_right = data.ranges[330:359]
    front_region.extend(front_left)
    front_region.extend(front_right)
    
    front_dist = min(front_region)

    left_region =  data.ranges[30:90]

    left_dist = min(left_region)



    right_region = data.ranges[270:330]

    right_dist = min(right_region)

    if front_dist > 10:
        front_dist = 10
   



    error_front  = threshold - front_dist
    if error_front > 0: 
    
        if right_dist > left_dist:
            move.angular.z = - 2*(error_front)
            #move.linear.x = 0.3
            move.linear.x = 0.5/(error_front + 1)
            pub.publish(move)
        else:
            move.angular.z = 2*(error_front)
        #move.linear.x = 0.3
            move.linear.x = 0.5/(error_front + 1)
            pub.publish(move)

    
    else:
        move.linear.x = vel
        move.angular.z = 0  
        rpub.publish(move)


def sort (unsorted_list):
    sorted_list = []
    for i in unsorted_list:
        if i > 1000:
            pass
        else:
            sorted_list.append(i)
    return sorted_list        







move = Twist() # Creates a Twist message type object
rospy.init_node('obstacle_avoidance_node') # Initializes a node
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  # Publisher object which will publish "Twist" type messages
                            				 # on the "/cmd_vel" Topic, "queue_size" is the size of the
                                                         # outgoing message queue used for asynchronous publishing

sub = rospy.Subscriber("/scan", LaserScan, callback)  # Subscriber object which will listen "LaserScan" type messages
                                                      # from the "/scan" Topic and call the "callback" function
						      # each time it reads something from the Topic
                       

rospy.spin() # Loops infinitely until someone stops the program execution