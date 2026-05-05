from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # 1. Base Controller: Translates cmd_vel to setpoints and receives effort
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

        # 2. Encoder Publisher: Provides raw feedback from the hardware
        Node(
            package='motor_controller',
            executable='encoder_publisher',
            name='encoder_publisher',
            output='screen',
            # Ensure these match what the PID nodes are remapped to
            remappings=[
                ('enc_l', '/left/encoder_raw'),
                ('enc_r', '/right/encoder_raw'),
            ]
        ),

        # 3. Left PID Node
        Node(
            package='motor_controller',
            executable='PID_control',
            name='left_pid',
            namespace='left',
            parameters=[{
                'kp' : 0.2,
                'ki' : 0.1,
                'kd' : 0.05,
            }],
            remappings=[
                ('enc', 'encoder_raw'),           # Links to encoder_publisher
                ('setpoint', 'setpoint'),         # Links to BaseController (/left/setpoint)
                ('control_effort', 'control_effort'), # Links to BaseController (/left/control_effort)
            ]
        ),

        # 4. Right PID Node
        Node(
            package='motor_controller',
            executable='PID_control',
            name='right_pid',
            namespace='right',
            parameters=[{
                'kp' : 0.2,
                'ki' : 0.1,
                'kd' : 0.05,
            }],
            remappings=[
                ('enc', 'encoder_raw'),           # Links to encoder_publisher
                ('setpoint', 'setpoint'),         # Links to BaseController (/right/setpoint)
                ('control_effort', 'control_effort'), # Links to BaseController (/right/control_effort)
            ]
        )
    ])