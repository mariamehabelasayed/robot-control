# robot-control
# 🚗 Midnight Tuner (ROS2 Jazzy)

A custom ROS2 Python package built for **Turtlesim** that acts as a tuner car simulator. It maps manual keyboard controls to non-holonomic velocity commands (`cmd_vel`) and processes real-time RGB values from the turtle's underglow color sensor to broadcast dominant color telemetry (`/dominant_color`).

---

## 🛠️ Features
* **Custom Keyboard Teleop:** Drive the turtle using throttle (`W`/`S`) and steering (`A`/`D`) inputs.
* **Neon Underglow Perception:** Subscribes to the turtlesim color sensor topic to analyze real-time RGB streams.
* **Dominant Color Telemetry:** Automatically classifies and publishes the primary underglow color (`RED`, `GREEN`, or `BLUE`) to a custom topic.
* **Modular Launch Integration:** Starts the simulation and controller node seamlessly using a ROS2 launch file.

---

## 🚀 Prerequisites & Installation

1. **Ensure ROS2 Jazzy and Turtlesim are installed:**
   ```bash
   sudo apt install ros-jazzy-turtlesim -y

**Clone or place the package into your workspace source directory:**
bash
    cd ~/tuner_ws/src

    **Build the workspace:**
    bash

    cd ~/tuner_ws
    colcon build --packages-select midnight_tuner

    **Source your environment:**
    bash

    source /opt/ros/jazzy/setup.bash
    source install/setup.bash

#🕹️ How to Run & Use
If your terminal capture requires a direct standard input stream for keyboard controls, run the nodes across two separate terminals:

    **Terminal 1 (Start Simulation):**
    bash

    source /opt/ros/jazzy/setup.bash
    ros2 run turtlesim turtlesim_node

    **Terminal 2 (Start Tuner Controller):**
    bash

    cd ~/tuner_ws
    source /opt/ros/jazzy/setup.bash
    source install/setup.bash
    ros2 run midnight_tuner tuner_controller

    (Click your mouse directly into Terminal 2 and use W, A, S, D to drive your turtle around!) 
