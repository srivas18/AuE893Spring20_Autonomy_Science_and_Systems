#### Course Name: AUE8930-Autonomy:Science and Systems
#### Assignment: Assignment 5: Tracking and Following
#### Team number: 4
#### Team Members: Ajinkya S Joglekar, R Manas Macherla, Satya Rahul Jaladi, Shailendran Poyyamozhi, Siddhant Srivastava

**Aim**: The aim of the assignment 5 was - 1. Manipulating image data for tracking a point. 2. Implementing path tracking controllers in Python.

We were given model files to create a line following environment in gazebo for Part 1. April tags were given for Part 2 and checkerboard was given for camera calibration.

Part 1 was asked to run on Gazebo environment as well as Real Turtlebot, whereas, Part 2 was asked to run on real Turtlebot.

--------------------------------------------------------------------------------------
###### Camera Calibration

This was accomplished by using the following commands after setting up the camera on the turtlebot3 burger robot:

note: the prefix 'pi@raspberrypi$' means the corresponding command must be run after doing ssh into the turtlebot raspberry pi computer.

$ roscore

pi@raspberrypi$ roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch

$ rosrun image_transport republish compressed in:=raspicam_node/image raw out:=raspicam_node/image_raw 

$ rosrun camera_calibration cameracalibrator.py --size 11x11 --square 0.017 image:=/raspicam_node/image camera:=/raspicam_node

Instructions were followed as per the below page: 
http://wiki.ros.org/camera_calibration
--------------------------------------------------------------------------------------

The assignment contains three launch files:

**Part 1a: "turtlebot3_follow_line.launch"**

- This file initializes the line following world in gazebo

- It launches the line follower python script as a node for detecting and following the yellow path in the given simulation world in gazebo

- The command for executing the above launch file is:

$ roslaunch assignment5_trackingandfollowing turtlebot3_follow_line.launch


**Part 1b: "turtlebot3_follow_line_realbot.launch"**

- This part shows the practical implementation of the line following functionality shown in the above part

- This requires setting up a turtlebot3 burger robot with a raspberry pi camera v2 

- The bot must be setup as a slave in a ROS network where a remote computer is the ROS master

- The following commands must be executed before runnning the above launch file (each command in a new terminal):

note: the prefix 'pi@raspberrypi$' means the corresponding command must be run after doing ssh into the turtlebot raspberry pi computer.

$ roscore

pi@raspberrypi$ roslaunch turtlebot3_bringup turtlebot3_robot.launch

pi@raspberrypi$ roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch

On remote machine follow the following codes:

$ rosrun image_transport republish compressed in:=raspicam_node/image raw out:=raspicam_node/image_raw

- Finally, the launch file can be executed: 

$ roslaunch assignment5_trackingandfollowing turtlebot3_follow_line_realbot.launch 


**Part 2: "april_tag_follow.launch"** 

- This part shows the practical implementation of detecting and following of the april tag by the turtlebot

- This requires setting up a turtlebot3 burger robot with a raspberry pi camera v2 

- The bot must be setup as a slave in a ROS network where a remote computer is the ROS master

- The following commands must be executed before runnning the above launch file (each command in a new terminal):

note: the prefix 'pi@raspberrypi$' means the corresponding command must be run after doing ssh into the turtlebot raspberry pi computer.

$ roscore

pi@raspberrypi$ roslaunch turtlebot3_bringup turtlebot3_robot.launch

pi@raspberrypi$ roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch

On remote machine follow the following codes:

$ rosrun image_transport republish compressed in:=raspicam_node/image raw out:=raspicam_node/image_raw
$ rqt_image_view 

- Finally, the launch file can be executed: 

$ roslaunch assignment5_trackingandfollowing april_tag_follow.launch 


Description
--------------------------------------------------------------------------------------

Team Contributions:
Camera setup in rasberrypi - Satya Rahul jaladi, R Manas Macherla, Shailendran Poyyamozhi
Camera Calibration - Ajinkya Jogelkar, Siddhant Srivastava
Line following implementation in Gazebo - Siddhant Srivastava, Manas Macherla, Satya Rahul Jaladi, Ajinkya Joglekar
Line following implementation on Real Turtlebot - Siddhant Srivastava, Shailendran Poyyamozhi, Satya Rahul Jaladi
April Tag implementation - Ajinkya Jogelkar, Shailendran Poyyamozhi
Launch file and Readme - Siddhant Srivastava, Ajinkya Jogelkar
Videos - Ajinkya Jogelkar, Satya Rahul Jaladi, Siddhant Srivastava

