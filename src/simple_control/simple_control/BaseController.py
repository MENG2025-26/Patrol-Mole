#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from simple_control.DcMotor import DCMotor as DCM


class BaseController(Node):

    def __init__(self):
        super().__init__('base_controller')

        # Parameters
        self.declare_parameter('max_pwm', 100.0)

        self.declare_parameter('leftForwardPin', 13)
        self.declare_parameter('leftBackwardPin', 19)
        self.declare_parameter('rightForwardPin', 18)
        self.declare_parameter('rightBackwardPin', 12)

        self.max_pwm = self.get_parameter('max_pwm').value

        lf = self.get_parameter('leftForwardPin').value
        lb = self.get_parameter('leftBackwardPin').value
        rf = self.get_parameter('rightForwardPin').value
        rb = self.get_parameter('rightBackwardPin').value

        # Motors
        self.left_motor = DCM(lf, lb)
        self.right_motor = DCM(rf, rb)

        # Subscriber
        self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_cb, 10)

        self.get_logger().info("Base Controller running")

    def cmd_vel_cb(self, msg: Twist):
        linear = msg.linear.x      # forward/back
        angular = msg.angular.z    # turning

        # Basic mixing (tank drive)
        left = linear - angular
        right = linear + angular

        # Normalize to keep within [-1, 1]
        max_mag = max(abs(left), abs(right), 1.0)
        left /= max_mag
        right /= max_mag

        # Scale to PWM
        left_pwm = left * self.max_pwm
        right_pwm = right * self.max_pwm

        # Clamp just in case
        left_pwm = max(min(left_pwm, self.max_pwm), -self.max_pwm)
        right_pwm = max(min(right_pwm, self.max_pwm), -self.max_pwm)

        # Send to motors
        self.left_motor.run(left_pwm)
        self.right_motor.run(right_pwm)

        self.get_logger().info(
            f"L PWM: {left_pwm:.1f} | R PWM: {right_pwm:.1f}"
        )

    def destroy_node(self):
        self.get_logger().info("Stopping motors...")
        self.left_motor.stop()
        self.right_motor.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = BaseController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down (Ctrl+C)")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()