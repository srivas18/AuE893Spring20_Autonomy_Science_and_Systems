#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Point, PoseArray
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3
from math import pow,atan2,sqrt
from sensor_msgs.msg import LaserScan
from turtlesim.msg import Pose
from darknet_ros_msgs.msg import BoundingBoxes
from people_msgs.msg import PositionMeasurementArray
from people_msgs.msg import PositionMeasurement
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import time


x = 0.0
y = 0.0
theta = 0.0
xp = 0.0
yp = 0.0
angle = 0
speed = 0
k_vel = 0.5
k_ang = 1.5
radius = 0.25
dist_r = 0
dist_front = 0
dist_l = 0
stop = False
stopped = False

min_dist = 100

lane_confirm = False

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()



    def camera_callback(self,data):
        
        # We select bgr8 because its the OpneCV encoding by default
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape
        msk = int(height/3)
        crop_img = cv_image[(height)/2+msk:(height)][1:width]
        
        # Convert from RGB to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        # Define the Yellow Colour in HSV

        """
        To know which color to track in HSV use ColorZilla to get the color registered by the camera in BGR and convert to HSV. 
        """

        # Threshold the HSV image to get only yellow colors
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Calculate centroid of the blob of binary image using ImageMoments
        m = cv2.moments(mask, False)

        global lane_confirm

        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
            lane_finder = False
            lane_confirm = True
        except ZeroDivisionError:
            cx, cy = height/2, width/2
            lane_finder = True

        res = cv2.bitwise_and(crop_img, crop_img, mask= mask)
        
        # Draw the centroid in the resultut image
       
        cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)

        cv2.imshow("Original", cv_image)
        cv2.imshow("MASK", mask)
        cv2.imshow("RES", res)
        cv2.waitKey(1)	
        global box
        global dur

        def stopcallback(data):

            for box in data.bounding_boxes:
                global stop

                if box.id == 11 and stop==False:

                            # t0 = rospy.get_time()
                    # pub_s=rospy.Publisher
                    # d=0
                    # print(t0)
                    # while(d<5):
                    # 	t1=rospy.get_time()
                    # 	pub_s=rospy.Publisher('cmd_vel',Twist,queue_size=10)
                    # 	move=Twist()
                    # 	move.linear.x=0
                    # 	move.angular.z=0
                    # 	pub_s.publish(move)
                    # 	d=t1-t0
                    # 	print(d)
                        #print("stop sign")
                     stop=True

                    #d=rospy.Duration(10,0)
                    #rospy.sleep(d)

                    #time.sleep(10)
                    #twist_object.angular.z = 0
                    #twist_object.angular.x = 0
                    #twist_object.angular.y = 0
                            #twist_object.linear.x = 0
                    #twist_object.linear.y = 0
                    #twist_object.linear.z = 0
                            #while (dur < 10.00):
                        #t1=float(rospy.Time.now().to_sec())
                        #dur=t1-t0
                                #twist_object.angular.z = 0
                                #twist_object.linear.x = 0
                        #twist_object.linear.y = 0
                        #twist_object.linear.z = 0
                        #twist_object.angular.x = 0
                        #twist_object.angular.y = 0
        def laser_callback(msg_laser):
                global min_dist
                ranges = msg_laser.ranges[1:90]
                min_dist = min(ranges)
                return min_dist


        rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,stopcallback)

        """
	Enter controller here.
        """
        if stop == False:
            # print('Non stop condition')
            error_x = cx - width / 2
            twist_object = Twist()
            # if error_x >-5 and error_x <5:
            #     error = 0
            twist_object.angular.z = -float(error_x/800)
            # temp = np.clip((-float(error_x/1000)), -0.2, 0.2)
            twist_object.linear.x = 0.1
        if stop == True:
            pose_sub = rospy.Subscriber('scan', LaserScan, laser_callback)
            global min_dist,stopped
            # print('Min dist is: ***************************************************************************************', min_dist)
            if min_dist > 0.18 and stopped == False:
                # print('Non stop condition')
                error_x = cx - width / 2
                twist_object = Twist()
                # if error_x >-5 and error_x <5:
                #     error = 0
                twist_object.angular.z = -float(error_x / 800)
                # temp = np.clip((-float(error_x/1000)), -0.2, 0.2)
                twist_object.linear.x = 0.1
            elif min_dist < 0.18 and stopped == False:
                t0 = rospy.get_time()
                stop_dur = 0
                while stop_dur < 3:
                    t1 = rospy.get_time()
                    twist_object = Twist()
                    twist_object.angular.z = 0
                    twist_object.linear.x = 0
                    self.moveTurtlebot3_object.move_robot(twist_object)
                    stop_dur = t1 - t0
                    stopped = True
            elif stopped == True:
                # print('Non stop condition')
                error_x = cx - width / 2
                twist_object = Twist()
                # if error_x >-5 and error_x <5:
                #     error = 0
                twist_object.angular.z = -float(error_x / 800)
                # temp = np.clip((-float(error_x/1000)), -0.2, 0.2)
                twist_object.linear.x = 0.1


        if lane_finder:
            if lane_confirm==False:
                # twist_object.linear.x = 0
                # twist_object.angular.z = -0.2

            ###########################################################################################################
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

                pose_subscriber = rospy.Subscriber('scan', LaserScan, callback)

                # rate = rospy.Rate(10)
                front = 0.8
                vel = 0.25
                # e = 0
                # while e < 1:
                    # twist_object.linear.x = 0
                    # twist_object.angular.z = -0.2

                error_front = front - dist_front
                if error_front > 0:
                        if dist_r > dist_l:
                            twist_object.angular.z = -2 * (error_front)
                            twist_object.linear.x = 0.15/(error_front + 1)
                            # pub.publish(twist_object)
                            # self.moveTurtlebot3_object.move_robot(twist_object)
                        else:
                            twist_object.angular.z = 2*(error_front)
                            twist_object.linear.x = 0.15/(error_front + 1)
                            # pub.publish(twist_object)
                            # self.moveTurtlebot3_object.move_robot(twist_object)

                else:
                    twist_object.linear.x = vel
                    twist_object.angular.z = 0
                    # pub.publish(twist_object)
                    # self.moveTurtlebot3_object.move_robot(twist_object)

                        ###########################################################################################
            if lane_confirm:
######################################### LEG DETECTION ######################################################
                def odo_value(msg):
                    global x
                    global y
                    global theta
                    x = msg.pose.pose.position.x
                    y = msg.pose.pose.position.y
                    orient = msg.pose.pose.orientation
                    (r, p, theta) = euler_from_quaternion([orient.x, orient.y, orient.z, orient.w])
                    theta = round(theta, 2)
                    return x, y

                def leg_callback(data):
                    # try:
                    global xp
                    global yp
                    global k_vel, k_ang, radius, angle, speed
                    try:
                        xp = data.poses[0].position.x
                        yp = data.poses[0].position.y
                    except IndexError:
                        xp = data.poses[1].position.x
                        yp = data.poses[1].position.y

                      
                    xp = round(xp, 2)
                    yp = round(yp, 2)

                    # velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
                    rate = rospy.Rate(10)
                    twist_object = Twist()
                    while sqrt(pow((xp - x), 2) + pow((yp - y), 2)) >= radius:
                        if (sqrt(pow((xp - x), 2) + pow((yp - y), 2))) > 0:
                            speed = min((sqrt(pow((xp - x), 2) + pow((yp - y), 2))), 1)
                        else:
                            pass
                        twist_object.linear.x = (k_vel) * speed

                        # angle = round((atan2(yp - y, xp - x) - theta), 2)
                        if (atan2(yp - y, xp - x) - theta) > 0:
                            angle = min((atan2(yp - y, xp - x) - theta), 1.5)
                        else:
                            angle = max((atan2(yp - y, xp - x) - theta), -1.5)
                        print(angle, "angle")
                        twist_object.angular.z = (k_ang) * angle
                        print(speed, "speed")
                        self.moveTurtlebot3_object.move_robot(twist_object)
                        rate.sleep()

                    twist_object.linear.x = 0
                    twist_object.angular.z = 0
                    self.moveTurtlebot3_object.move_robot(twist_object)

                # rospy.init_node('vel_closed', anonymous=True)
                cv2.destroyAllWindows()
                leg_subscriber = rospy.Subscriber('/to_pose_array/leg_detector', PoseArray, leg_callback)
                pose_subscriber_leg = rospy.Subscriber('odom', Odometry, odo_value)
                pose = Pose()
                rospy.spin()

                # twist_object.linear.x = 0
                # twist_object.angular.z = 0

        # Make it start turning
        self.moveTurtlebot3_object.move_robot(twist_object)
        
    def clean_up(self):
        self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()
        
        

def main():
    rospy.init_node('line_following_node', anonymous=True)
    
    
    line_follower_object = LineFollower()

    
    rate = rospy.Rate(5)
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        rate.sleep()

    
    
if __name__ == '__main__':
    rospy.sleep(20)
    main()
