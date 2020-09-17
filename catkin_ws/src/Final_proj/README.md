#### Course Name: AUE8930-Autonomy:Science and Systems
#### Project: Final Project
#### Team number: 4
#### Team Members: Ajinkya S Joglekar, R Manas Macherla, Satya Rahul Jaladi, Shailendran Poyyamozhi, Siddhant Srivastava

**Aim**: The aim of the project is to amalgamate the learnings of the previous assignments like wall following, onstacle avoidance and line following with the addition of traffic sign detection and people tracker. The final outcome was to finish the whole course while completing the following three tasks given:
1. Task 1: Wall following/Obstacle avoidance - The Turtlebot starts here. It must successfully follow the wall and avoid the obstacles until it reaches the yellow line. Create a map of this corridor using a SLAM package of our choice.
2. Task 2: Line following - The Turtlebot must successfully follow the yellow line. 
	a. Stop Sign detection - While navigating the yellow line, the the Turtlebot should stop at the stop sign for 3 seconds before continuing. The stop-sign will be detected by TinyYOLO.
3. Task 3: Human tracking - The Turtlebot must use a trained DL network to identify the human in the environment and follow it around (handout pending). The human in Gazebo can be teleoperated around using the keyboard. This teleoperation is already part of the given Gazebo environment.

--------------------------------------------------------------------------------------
###### PI CAMERA ADDITION

NOTE: PI CAMERA ADDITION TO TURTLEBOT3 BURGER IN GAZEBO For the simulation part of this assignemnt in gazebo, the turtlebot3 burger model was used in keeping with the trend of using the actual model provided to the group for real life implementation. Hence, the pi camera configuration settings were added to the burger model .xacro files in the below path (where catkin_ws is the name of the workspace where the relevatn turtlebot3 packages are installed):

/catkin_ws/src/turtlebot3/turtlebot3_description

for runnning the below (part 1a) files correctly, the following two files in the above path must be added (replace existing files with below files):

turtlebot3_burger.gazebo.xacro turtlebot3_burger.urdf.xacro


--------------------------------------------------------------------------------------
###### TINY YOLO PACKAGE INSTALLATION

Tiny Yolo package was installed from https://github.com/leggedrobotics/darknet_ros

The pretrained models (on the COCO dataset) here https://pjreddie.com/darknet/yolo/ have already been trained on "Stop Signs" as part of the larger dataset.

This ROS package encapsulates all the detection code in a blackbox format and simply publishes the label for the stop sign detection as a rostopic.

The detected rostopic for the stop sign was used to stop the robot for 3 seconds before the stop sign in Gazebo.

--------------------------------------------------------------------------------------

###### LEG DETECTION

For implementing the human tracker, the People Detection packing was provided with the handout 8.

the packages namely 'people', 'person_sim', 'tc_people_tracker' and 'detector_msg_to_pose_array', were added into the workspace.


The assignment contains one launch file.

**"final_code_revised.launch"**

- This file initializes the gazebo world given with stop sign, line follow and person.

- It launches the tiny yolo launch package.

- It launches leg detector and people tracker launch package.

- It launches the node package **"final_one.py"** which executes the robot to complete the course and complete the aforementioned three tasks autonomously. The switching between the completion of each task is done automatically.

$ roslaunch fin_proj final_code_revised.launch

The above command in the terminal launches the whole environment and code in Gazebo world.

Alternatively, we had also created a backup code framework which initializes eack code with a keyboard press.
--------------------------------------------------------------------------------------

Team Contributions:
Camera addition in Burger - Siddhant Srivastava
Wall Following, Obstacle avoidance and SLAM (Gmapping) - Satya Rahul Jaladi, Shailendran Poyyamozhi
Line Following - R Manas Macherla
Yolo stop sign detection and stopping - Shailendra Poyyamozhi, Ajinkya Jogelkar, Siddhant Srivastava
Leg detection - R Manas Macherla, Ajinkya Jogelkar, Satya Rahul Jaladi
Code Integration - Satya Rahul Jaladi, Ajinkya Jogelkar, Shailendra Poyyamozhi
Code Tuning - Satya Rahul Jaladi, Siddhant Srivastava, R Manas Macherla
Launch File creation - Shailendra Poyyamozhi, Siddhant Srivastava, Ajinkya Jogelkar
