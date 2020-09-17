#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.14 
speed = 0.2
angular_speed = 0.2

def make_square():
  print('Making a square')
  rospy.init_node('turtlesim_square', anonymous=True)
  vel_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size = 10)
  vel_msg = Twist()
  side_legnth = 2

  current_rotation = 0
  while current_rotation < 4:
    move_in_line(side_legnth,vel_msg,vel_publisher)
    rotate(vel_msg,vel_publisher)
    current_rotation+=1

  rospy.spin()  

def move_in_line(side_legnth,vel_msg,vel_publisher):
  vel_msg.linear.x = speed
  # vel_msg.linear.y = 0
  # vel_msg.linear.z = 0
  # vel_msg.angular.x = 0
  # vel_msg.angular.y = 0
  # vel_msg.angular.z = 0

  t0 = rospy.Time.now().to_sec()
  distance_travelled = 0

  while distance_travelled < side_legnth:
    vel_publisher.publish(vel_msg)
    print(vel_msg.linear.x)
    t1 = rospy.Time.now().to_sec()
    distance_travelled = speed * (t1-t0)

  vel_msg.linear.x = 0  
  vel_publisher.publish(vel_msg)  


def rotate(vel_msg,vel_publisher):
  vel_msg.angular.z = angular_speed
  t0  = rospy.Time.now().to_sec()
  angle_travelled = 0

  while (angle_travelled < PI/2.0):
    vel_publisher.publish(vel_msg)
    t1 = rospy.Time.now().to_sec()
    angle_travelled = angular_speed * (t1 - t0)

  vel_msg.angular.z = 0  
  vel_publisher.publish(vel_msg)  
     

if __name__ == '__main__':
    try:
      make_square()
    except rospy.ROSInterruptException:
      pass  
