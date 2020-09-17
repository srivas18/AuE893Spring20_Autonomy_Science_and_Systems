#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3

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
        crop_img = cv_image[(height)/2+180:(height)/2+200][1:width]
        
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
        
        """
	Enter controller here.
        """
        error_x = cx - width / 2
        twist_object = Twist()
        if error_x >-5 and error_x <5:
            error = 0
        twist_object.angular.z = np.clip((-float(error_x/1000)), -0.2, 0.2)
        temp = np.clip((-float(error_x/1000)), -0.2, 0.2)
        twist_object.linear.x = np.clip(0.2*(1-abs(temp)/0.2), 0, 0.08)

        if lane_finder:
            if lane_confirm==False:
                twist_object.linear.x = 0.1
                twist_object.angular.z = -0.02

            if lane_confirm:
                twist_object.linear.x = 0.08
                twist_object.angular.z = 0.21

        rospy.loginfo("ANGULAR VALUE SENT===>"+str(twist_object.angular.z))
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
    main()
