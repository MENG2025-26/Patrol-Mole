#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

import sys
import termios
import tty


class CustomTeleop(Node):

    def __init__(self):
        super().__init__('custom_teleop')

        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.arm_pub = self.create_publisher(Float32, 'arm_cmd', 10)

        self.speed = 0.8   # adjust drive speed here
        self.arm = 0.0

        self.get_logger().info("WASD drive | Y/H arm | N stop arm")

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def run(self):
        while True:
            key = self.get_key()

            twist = Twist()
            arm_msg = Float32()

            # DRIVE
            if key == 'w':
                twist.linear.x = self.speed
            elif key == 's':
                twist.linear.x = -self.speed
            elif key == 'a':
                twist.angular.z = self.speed
            elif key == 'd':
                twist.angular.z = -self.speed
            elif key == ' ':
                twist.linear.x = 0.0
                twist.angular.z = 0.0

            # ARM
            elif key == 'y':
                self.arm = 1.0
            elif key == 'h':
                self.arm = -1.0
            elif key == 'n':
                self.arm = 0.0

            elif key == '\x03':
                break

            self.cmd_pub.publish(twist)

            arm_msg.data = self.arm
            self.arm_pub.publish(arm_msg)


def main(args=None):
    global settings

    settings = termios.tcgetattr(sys.stdin)

    rclpy.init(args=args)
    node = CustomTeleop()

    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
