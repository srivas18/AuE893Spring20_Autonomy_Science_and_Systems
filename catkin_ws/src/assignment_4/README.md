_Course Name: AUE8930-Autonomy:Science and Systems_
_Assignment: Assignment 4: Obstacle Avoidance_
_Team number: 4_
_Team Members: Ajinkya S Joglekar, R Manas Macherla, Satya Rahul Jaladi, Shailendran Poyyamozhi, Siddhant Srivastava_

_Aim_: The aim of the assignment 4 was - 1. Manipulating scan data for navigation. 2. Implementing P or PD controllers in Python.

We were given 2 world files "Wall Following" and "Obstacle Avoidance". We were needed to generate two scripts for the Turtlebot 3 Burger to implement wall following and obstacle avoidance. The final script needed to be run in this world files in Gazebo to test our code.

Finally, we were asked to run the Object avoidance code on actual turtlebot 3 burger. Our turtlebot ran perfectly and the videos are attached for the same.

_Codes:_
_wallfollower.py_ - The code contains a PD controller to help mitigate any error in the scan data and give that error free input as angular velocity so that the Turtlebot maintains equidistance with the walls on both the sides, when it is moving at a straight line. The forward velocity in this case was kept at 0.5 m/s.
If the bot approaches a turn then error was calculated between left and right scan data and the angular velocity was calculated as 1.5 times the summation of forward error 'error_front' (difference between 1.4 m and front distance = 10 m). The forward velocity was kept at 0.25 m/s when the bot is taking a turn.

_wander.py_ - The code contains the scan data of the front region for an angle of 60 deg segregating as 30 deg and 30 deg. The left and right regions were scanned for 60 degrees each. The front distance was captured as minimum value of the front region scan data. If the front distance was more than 10 then the front distance was capped to 10 to remove any infinity values. Error was calculated to remove any zero values by measuring the difference between threshold value and front distance value. The threshold value was kept as 1. As the bot approaches an obstacle it takes left or right turn as per the left and right region scanned data and comparison between their distance values.


Necessary Commands:
1. "roslaunch assignment_4 turtlebot3_wallfollowing.launch" - Command in the terminal to initiate the launch file that will open the wall following world and runs the wallfollower.py script in gazebo
2. "roslaunch assignment_4 turtlebot3_obstaceavoidance.launch" - Command in the terminal to initiate the launch file that will open the obstacle avoidance world and runs the wander.py script in gazebo

Team Contributions:
Scripts for Assignment 3: Ajinkya Joglekar, Satya Rahul Jaladi, R Manas Macherla, Siddhant Srivastava, Shailendran Poyyamozhi
Launch Files: Ajinkya Joglekar, Shailendran Poyyamozhi, R Manas Macherla
World Files: Ajinkya Joglekar, Siddhant Srivastava, Satya Rahul Jaladi
Videos and Readme Files: Siddhant Srivastava, Shailendran Poyyamozhi
Git Version Control: Ajinkya Joglekar

