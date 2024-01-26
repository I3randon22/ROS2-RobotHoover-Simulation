# ROS2-RobotHoover-Simulation
ROS2 launch file and related configurations for simulating a robot hoover. The simulation integrates various ROS2 components and tools, providing a comprehensive setup for robot operation and interaction within the Gazebo simulation environment.

## Overview

This simulation showcases a robot hoover operating in a Gazebo environment, featuring sensor integration for a more comprehensive simulation experience.

### Sensors Included:

- **IMU (Inertial Measurement Unit)**: Integrated to provide orientation and motion data.
- **Lidar Sensor**: Included for environmental mapping and obstacle detection.
- **Depth Camera**: Added for enhanced environmental perception.

### Additional Features:

- **Gazebo Simulation**: A dynamic and interactive simulation environment for the robot hoover.
- **Teleoperation**: Allows manual control of the robot hoover using keyboard inputs.
- **Twist Mux**: Manages multiple control input sources efficiently.

## Key Functionalities

- **Robot State Publisher**: Publishes the robot's state in the simulation environment using its URDF model.
- **Sensor Data Integration**: Incorporates data from the IMU, Lidar, and depth camera, enriching the simulation's capabilities.
- **Teleoperation and Command Management**: Provides manual control over the robot hoover and prioritizes command sources.

## Usage

To get started with the robot hoover simulation:

1. Ensure ROS2, Gazebo, and necessary ROS2 packages are installed.
2. Clone this repository.
3. Launch the simulation using:
   ```bash
   ros2 launch seaborgium_sim_bringup.launch.py
