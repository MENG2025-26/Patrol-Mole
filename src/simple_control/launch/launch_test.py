from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    base_controller = Node(
        package='simple_control',
        executable='BaseController',
        name='base_controller',
        output='screen',
        parameters=[
            {'max_pwm': 50.0}
        ]
    )

    teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop',
        prefix=['xterm -e gdb -ex run --args'],
        output='screen',
    )

    return LaunchDescription([
        base_controller,
        teleop
    ])