Course Name: AUE8930-Autonomy:Science and Systems
Assignment: Assignment 3
Team number: 4
Team Members: Ajinkya S Joglekar, R Manas Macherla, Satya Rahul Jaladi, Shailendran Poyyamozhi, Siddhant Srivastava

Aim: The assignment 3 was first of the many group/team assignments with the aim to run the 'circle.py' and 'square.py' codes done assignment 2, in 3D simulation environment (Gazebo) with minor modification in the code. A launch file named 'move.launch' was created which would bring up the turtlebot burger in Gazebo environment and simulating either of the two codes after mentioning it in the terminal.
Another part of the assignment was to create a world in gazebo named 'turtlebot3_wall.world' with a wall in it for turtlebot burger. A python code named 'question_3.py' was created that published constant linear velocity to /cmd.vel. The code also subscribed to the /scan topic and extracted the centre-most value of the scanned data array. A launch file was created named 'turtlebot3_wall.launch' which would launch the turtlebot burger in gazebo environment and simulate the script.

Necessary Commands:
1. "roslaunch assignment_3 move.launch code:=square" (This command in terminal runs 'square.py' script in Gazebo) - The Turtlebot 3 burger traces a square of length 2 m with a linear speed of 0.2 m/s and turning at the vertices with the angular velocity of 0.2 rad/s.
2. "roslaunch assignment_3 move.launch code:=circle" (This command in terminal runs 'circle.py' script in Gazebo) - The Turtlebot 3 burger traces a circular path of radius 2 m with angular velocity of 1.57 rad/s and linear velocity of 0.2 m/s.
3. "roslaunch assignment_3 turtlebot3_wall.launch code:=question_3" (This command in terminal launches 'turtlebot3_wall.world' and runs 'question_3.py' script in Gazebo) - The Turtlebot 3 burger runs straight towards a wall at a linear velocity of 0.5 m/s and stops 2 m before the wall after scanning the obstruction.

Team Contributions:
Scripts for Assignment 3: Ajinkya Joglekar, Satya Rahul Jaladi, R Manas Macherla
Launch Files: Ajinkya Joglekar, Shailendran Poyyamozhi, R Manas Macherla
World Files: Ajinkya Joglekar, Siddhant Srivastava, Satya Rahul Jaladi
Videos and Readme Files: Siddhant Srivastava, Shailendran Poyyamozhi
Git Version Control: Ajinkya Joglekar

