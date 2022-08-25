# Classification of User-specific Symbols for Intuitive Control Using CNN
**Marshall Johnson**  
**MSR Final Project**  
**Advisors: Matthew Elwin, PhD and Ola Kalinowska**  

## Overview
The primary objective of this project was to classify [sip-and-puff (SNP)](https://www.orin.com/access/sip_puff/#Sip/Puff%20Breeze) signals into user-defined symbols to generate an intuitive set of controls. The application of this technology would be particularly useful to someone who lacks the ability to use their hands. This project allows for the creation of a custom set of controls using an SNP sensor in a short amount of time. 

## Process
1. To begin, a user must complete a set of simulated mazes that can be viewed through RViz and/or Gazebo.   
*Note: Though the user feels as if they are in control of the robot, the robot control is predefined based on the maze generated. Future development would allow for the user to affect robot behavior as they progress through the maze curriculum.*
2. The inputs a user provides to complete this maze are collected to train a neural network sepcific to that user.
3. User data is augmented to increase the size of the dataset, reducing the need for a more time intensive data collection process with the user. 
4. The augmented dataset is used to train a 1-dimensional convolutional neural network (CNN) to classify SNP inputs into discrete movement actions (forward, left, right, stop).
5. Using the trained network, the user can navigate the Gazebo world freely, and eventually, real life.

## Contents

### Nodes
- `maze`: Responsible for generating maze in simulated Rviz/Gazebo environment. Subscribes to sip and puff input and auto-labels user data during simulation run. Can also be run without maze to speed up data collection process. 
- `data_collection`: Collects and publishes data from sip and puff sensor to be used by `maze` node.

### Helper Files
- `cnn.py`: Neural network used to classify sip and puff signals (1D CNN)
- `data_augmentation.py`: Contains functions used to augment user data. Generates large dataset from small original sample to facilitate model training and reduce time required from user.
- `generate_maze.py`: Generates maze of variable difficulty from preset tiles. Creates path through maze for robot to follow.
- `synthetic.py`: Generate and test synthetic dataset. Primarily used to test/verify machine learning pipeline.

## Usage Instructions
### Simulation
Collect user sip and puff input while running maze simulation:  
1. `roslaunch maze_gen maze.launch`  
Launches a turtlebot in the simulated environment with `sim` as the control mode.
2. `rosservice call \generate_maze`  
Generates maze and creates markers in Rviz and Gazebo to display.
3. `rosservice call \move`
Starts turtlebot in motion and initiates sip and puff data collection.
4. `rosservice call \process_data`  
Process sip and puff data for csv output.
5. `rosservice call \save_data`  
Save processed data as csv.

### Data Collection Only
Collect data from sip and puff without running maze simulation:  
1. `roslaunch maze_gen maze.launch`  
Launch simulated environment (Control mode does not matter. Can also be run with control:=manual)  
2. `rosservice call \collect_data`  
Will save the latest sip and puff input received and prompt for ground truth value. Input ground truth with keyboard and press Enter.   
*Note: Make sure to sip/puff into sensor prior to this step.*
3. `rosservice call \save_data`  
Save labeled data to csv.  

### Testing Trained Model
Use trained model to move turtlebot through maze simulation:  
1. Ensure path to desired model is correct in the `load_model` function of the `maze` node.
2. `roslaunch maze_gen maze.launch control:=manual`  
Launches a turtlebot in the simulated environment with `manual` as the control mode.  
3. `rosservice call \generate_maze`  
Generates maze and creates markers in Rviz and Gazebo to display.  
4. Provide sip and puff input. Model will make predictions and translate into corresponding movement actions represented by the turtlebot in simulation. 

### Optional Services
- `rosservice call \print_data`  
Prints data collected along with labels
- `rosservice call \reset`  
Resets simulation and data to run another trial.  
- `rosservice call \toggle_control_mode`  
Toggles control mode between `sim` and `manual`. Running this service will switch to whichever control mode is not currently being used.

More coming soon...