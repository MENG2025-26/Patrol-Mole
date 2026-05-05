from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([


        # Left Wall Sensor
        Node(
            package='tof_sensors',
            executable='tofsensor',
            namespace='left',
            parameters=[{
                'i2c_address': 0x32,
                'xshut_pin': 20,
                'frame_id': 'wall_sensor_left_link'
            }]
        ),

        # Right Wall Sensor
        Node(
            package='tof_sensors',
            executable='tofsensor',
            namespace='right',
            parameters=[{
                'i2c_address': 0x33,
                'xshut_pin': 21,
                'frame_id': 'wall_sensor_right_link'
            }]
        ),

    ])
