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

## 

More coming soon...
