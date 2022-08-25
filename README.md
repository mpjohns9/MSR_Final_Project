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
To run the maze simulation with a user providing input, follow the steps below:  
1. 

More coming soon...
