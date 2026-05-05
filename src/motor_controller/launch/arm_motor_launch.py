from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # BASE CONTROLLER (WITH REMAPPING!)
        Node(
            package='motor_controller',
            executable='BaseController',
            name='base_controller',
            output='screen',
            remappings=[
                ('lsetpoint', '/left/setpoint'),
                ('rsetpoint', '/right/setpoint'),
                ('lcontrol_effort', '/left/control_effort'),
                ('rcontrol_effort', '/right/control_effort'),
            ],
        ),

        # ENCODER
        Node(
            package='motor_controller',
            executable='encoder_publisher',
            name='encoder_publisher',
            output='screen',
            remappings=[
                ('enc_l', '/left/encoder_raw'),
                ('enc_r', '/right/encoder_raw'),
            ]
        ),

        # LEFT PID
        Node(
            package='motor_controller',
            executable='PID_control',
            name='left_pid',
            namespace='left',
            parameters=[{'kp': 0.5, 'ki': 0.0, 'kd': 0.00}],
            remappings=[
                ('enc', 'encoder_raw'),
                ('setpoint', 'setpoint'),
                ('control_effort', 'control_effort'),
            ]
        ),

        # RIGHT PID
        Node(
            package='motor_controller',
            executable='PID_control',
            name='right_pid',
            namespace='right',
            parameters=[{'kp': 1.5, 'ki': 0.2, 'kd': 0.00}],
            remappings=[
                ('enc', 'encoder_raw'),
                ('setpoint', 'setpoint'),
                ('control_effort', 'control_effort'),
            ]
        ),

        # ARM
        Node(
            package='motor_controller',
            executable='armcontrol',
            name='arm_control',
            output='screen',
            parameters=[{
                'max_pwm': 120.0,
                'ForwardPin': 5,
                'BackwardPin': 6,
            }],
        ),
    ])
