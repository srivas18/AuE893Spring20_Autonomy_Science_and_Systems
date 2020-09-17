#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg  import Twist, Point
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
from sensor_msgs.msg import LaserScan
import numpy as np
import roslaunch

import time
wall_follow_exec = 0
line_follow_exec = 0
leg_follow_exec = 0
stop_exec = 0
mode = 'n'


def listener():
    rospy.init_node('main_scr', anonymous=True)
    rospy.Subscriber('/keypress', String, callback)
    # rospy.spin()


def callback(data):
    global mode
    if data.data:
        mode = data.data
    else:
       pass

# def wall():
#     print('Wall follow *****************************************************************************************')
def stop():
    t0 = rospy.get_time()
    dur = 0
    while dur < 1:
        t1 = rospy.get_time()
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        move = Twist()
        move.linear.x = 0
        move.angular.z = 0
        pub.publish(move)
        # print('Stopped')
        dur = t1 - t0

def mode_select():
    global wall_follow_exec,line_follow_exec,stop_exec,leg_follow_exec,mode
    while not rospy.is_shutdown():
        if mode == 'w' and wall_follow_exec == 0:
            # print('Wall exec', wall_follow_exec)
            uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
            roslaunch.configure_logging(uuid)
            launch = roslaunch.parent.ROSLaunchParent(uuid,["/home/ajoglek/AuE893_Spring20_Ajinkya_Joglekar/catkin_ws/src/fin_proj/launch/obstacle.launch"])
            launch.start()
            # rospy.loginfo(" Wall and obstcale avoid started")
            wall_follow_exec = 1
        elif mode == 'l' and line_follow_exec == 0:
            stop()
            launch.shutdown()
            # print('Transition betn obstacle and line follow')
            uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
            roslaunch.configure_logging(uuid)
            launch_line = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ajoglek/AuE893_Spring20_Ajinkya_Joglekar/catkin_ws/src/fin_proj/launch/line_follow.launch"])
            launch_line.start()
            # rospy.loginfo(" Line follower started")
            line_follow_exec = 1
            #image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, camera_callback)
        elif mode == 'p' and leg_follow_exec == 0:
            launch_line.shutdown()
            stop()
            # print('Transition betn line follow and leg detection')
            uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
            roslaunch.configure_logging(uuid)
            launch_leg = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ajoglek/AuE893_Spring20_Ajinkya_Joglekar/catkin_ws/src/People_Detection/tc_people_tracker/people_tracker_tc/launch/leg_detector_start.launch"])
            launch_leg.start()
            # rospy.loginfo(" Leg follower started")
            leg_follow_exec = 1
            #image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, camera_callback)
        elif mode =='s' and stop_exec == 0:
            # print('Performing shutdown')
            stop()
            launch_leg.shutdown()
            stop_exec = 1
        else:
            pass

if __name__ == '__main__':
        listener()
        mode_select()
        # cam()
