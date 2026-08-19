from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='midnight_tuner',
            executable='tuner_controller',
            name='tuner_controller_node',
            output='screen',
            parameters=[{
                'cmd_vel_topic': '/turtle1/cmd_vel',
                'color_sensor_topic': '/turtle1/color_sensor',
                'dominant_color_topic': '/dominant_color'
            }]
        )
    ])

