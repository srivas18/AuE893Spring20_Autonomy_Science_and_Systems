This file provides for an overview of the scripts in the second assignment.
These files can be found in assignment_2 package.

Explaination of files in the src folder

circle.py: This file acts like a client file to send request to the make_circle_server.py with the speed and radius of the circle. In return it receives the Twist messages to run the turtlebot in the desired trajectory.

make_circle_server.py: This script intializes the service with service type 'MakeCircle' and function process_make_circle to take the inputs from the circle.py file and publish the linear.x and angular.z Twist messages to the turtlesim.

square_openloop.py: This is a simple python file that makes the turtle trace a rectangular trajectory. Using the make_square function, the turtlebot executes the moving in line and rotation of 90 degrees in a loop for four times to trace the rectangle. If we have any other regular polygon, only changing the angle per each rotation will help to trace trajectory of that polygon.


square_closedloop.py: This code is similiar to the one above but the primary difference is that we also subscribe to the pose of the turtle at every time step. Using this pose, we can have a closed loop system governed by a proportional controller for navigating to the desired co-ordinate. This is done with the help of 'go_to_goal' function. Additionally, if we want to trace a sqaure trajectory with the help of four co-ordinate points, we need to orient the turtle towards over next co-ordinate point in order to trace a straight line as optimum path. In the code this is done by the 'setDesiredOrientation' function.
