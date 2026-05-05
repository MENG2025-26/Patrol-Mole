#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

from simple_control.DcMotor import DCMotor as DCM


class ArmControl(Node):

    def __init__(self):
        super().__init__('armcontrol')

        self.declare_parameter('max_pwm', 120.0)
        self.declare_parameter('ForwardPin', 5)
        self.declare_parameter('BackwardPin', 6)

        self.max_pwm = self.get_parameter('max_pwm').value

        f = self.get_parameter('ForwardPin').value
        b = self.get_parameter('BackwardPin').value

        self.arm_motor = DCM(f, b)

        self.create_subscription(Float32, 'arm_cmd', self.arm_cb, 10)

        self.get_logger().info("Arm Control running")

    def arm_cb(self, msg: Float32):
        arm_input = max(min(msg.data, 1.0), -1.0)
        pwm = arm_input * self.max_pwm

        self.arm_motor.run(pwm)

        self.get_logger().info(f"Arm PWM: {pwm:.1f}")

    def destroy_node(self):
        self.get_logger().info("Stopping arm motor...")
        self.arm_motor.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ArmControl()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
