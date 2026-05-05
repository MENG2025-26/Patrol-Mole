#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64, Bool
from geometry_msgs.msg import Twist

from motor_controller.DcMotor import DCMotor as DCM


class BaseController(Node):

    def __init__(self):
        super().__init__('base_controller')

        self._leftPWM = 0.0
        self._rightPWM = 0.0

        self.speed = 0.0
        self.spin = 0.0

        self.declare_parameter('leftMaxRPM', 100.0)
        self.declare_parameter('rightMaxRPM', 100.0)
        self.declare_parameter('wheel_diameter', 0.084)
        self.declare_parameter('wheel_base', 0.252)
        self.declare_parameter('leftTicksPerRotation', 980.0)
        self.declare_parameter('rightTicksPerRotation', 980.0)

        self.declare_parameter('leftForwardPin', 13)
        self.declare_parameter('leftBackwardPin', 19)
        self.declare_parameter('rightForwardPin', 18)
        self.declare_parameter('rightBackwardPin', 12)

        self._wheel_diameter = self.get_parameter('wheel_diameter').value
        self._wheel_base = self.get_parameter('wheel_base').value
        self._leftTPR = self.get_parameter('leftTicksPerRotation').value
        self._rightTPR = self.get_parameter('rightTicksPerRotation').value

        self._lfPin = self.get_parameter('leftForwardPin').value
        self._lbPin = self.get_parameter('leftBackwardPin').value
        self._rfPin = self.get_parameter('rightForwardPin').value
        self._rbPin = self.get_parameter('rightBackwardPin').value

        self._leftWheel = DCM(self._lfPin, self._lbPin)
        self._rightWheel = DCM(self._rfPin, self._rbPin)

        self.create_subscription(Float64, 'lcontrol_effort', self.lmotor_cb, 10)
        self.create_subscription(Float64, 'rcontrol_effort', self.rmotor_cb, 10)
        self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_cb, 10)

        self.lsetpoint_pub = self.create_publisher(Float64, 'lsetpoint', 10)
        self.rsetpoint_pub = self.create_publisher(Float64, 'rsetpoint', 10)
        self.lpid_enable_pub = self.create_publisher(Bool, 'lpid_enable', 10)
        self.rpid_enable_pub = self.create_publisher(Bool, 'rpid_enable', 10)

        self.publish_setpoints(0.0, 0.0)

    def cmd_vel_cb(self, msg: Twist):
        self.speed = msg.linear.x
        self.spin = msg.angular.z
        self.set_motor_speeds()

    def lmotor_cb(self, msg: Float64):
        self._leftWheel.run(max(min(msg.data, 100.0), -100.0))

    def rmotor_cb(self, msg: Float64):
        self._rightWheel.run(max(min(msg.data, 100.0), -100.0))

    def set_motor_speeds(self):

        if self.speed == 0.0 and self.spin == 0.0:
            left = 0.0
            right = 0.0
            self._leftWheel.stop()
            self._rightWheel.stop()
        else:
            right_twist = self.spin * self._wheel_base / self._wheel_diameter
            left_twist = -self.spin * self._wheel_base / self._wheel_diameter

            left_mps = self.speed + left_twist
            right_mps = self.speed + right_twist

            left_rpm = (left_mps * 60.0) / (math.pi * self._wheel_diameter)
            right_rpm = (right_mps * 60.0) / (math.pi * self._wheel_diameter)

            left = (left_rpm / 1200.0) * self._leftTPR
            right = (right_rpm / 1200.0) * self._rightTPR

        self.publish_setpoints(left, right)

    def publish_setpoints(self, left, right):
        self.lsetpoint_pub.publish(Float64(data=left))
        self.rsetpoint_pub.publish(Float64(data=right))


def main():
    rclpy.init()
    node = BaseController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
