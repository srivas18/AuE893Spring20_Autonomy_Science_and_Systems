#!/usr/bin/env python

from __future__ import print_function

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist,Pose

import sys, select, termios, tty
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
from sensor_msgs.msg import LaserScan
import numpy as np


msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >
t : up (+z)
b : down (-z)
anything else : stop
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
CTRL-C to quit
"""

moveBindings = {
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'u':(1,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

dist_r = 0
dist_front = 0
dist_l = 0

def callback(msg):
    global dist_r
    global dist_front
    global dist_l
    distances = []
    distances_front = []
    distances_l = []
    head1 = msg.ranges[1:16]
    head2 = msg.ranges[344:359]
    tail = msg.ranges[280:330]
    left = msg.ranges[30:80]
    distances_front.extend(head1)
    distances_front.extend(head2)
    distances.extend(tail)
    distances_l.extend(left)
    dist_r = sum(distances)/len(distances)
    dist_l = sum(distances_l)/len(distances_l)
    dist_front = min(distances_front)
    if dist_front > 10:
    	dist_front = 10


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
    rospy.init_node('teleop_twist_keyboard')

    speed = rospy.get_param("~speed", 0)
    turn = rospy.get_param("~turn", 0)
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        print(msg)
        # print(vels(speed,turn))
        while(1):
            key = getKey()
            # if key in moveBindings.keys():
            #     x = moveBindings[key][0]
            #     y = moveBindings[key][1]
            #     z = moveBindings[key][2]
            #     th = moveBindings[key][3]
            # elif key in speedBindings.keys():
            #     speed = speed * speedBindings[key][0]
            #     turn = turn * speedBindings[key][1]

            #     print(vels(speed,turn))
            #     if (status == 14):
            #         print(msg)
            #     status = (status + 1) % 15
            if key == 'y':
            	''' Start obstacle avoidance'''
            	print('Start of obstacle avoidance')
            	pose_subscriber = rospy.Subscriber('scan', LaserScan, callback)
            	twist = Twist()
            	front = 0.9
            	vel = 0.25
            	z = 1
            	e = 0
            	while e < z:
            		error_front = front - dist_front
            		if error_front > 0:
    			    	if dist_r > dist_l:
    			    		twist.angular.z = -2*(error_front)
    			    		twist.linear.x = 0.17/(error_front + 1)
    			    		pub.publish(twist)
    			        else:
    			        	twist.angular.z = 2*(error_front)
    			        	twist.linear.x = 0.17/(error_front + 1)
    			        	pub.publish(twist)
    			    # else:
    			    # 	twist.linear.x = vel
    			    # 	twist.angular.z = 0
    			    # 	pub.publish(move)    	
    			
            	'''End Obstacle Avoidance ''' 
            elif key == 'z':
            	print('z pressed')	 
            else:
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break

            twist = Twist()
            twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th*turn
            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
