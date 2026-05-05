#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32, Float64


class SimplePID(Node):

    def __init__(self):
        super().__init__('basic_pid')

        # -------- parameters --------
        self.declare_parameter('kp', 0.1)
        self.declare_parameter('ki', 0.0)
        self.declare_parameter('kd', 0.0)

        self.kp = self.get_parameter('kp').value
        self.ki = self.get_parameter('ki').value
        self.kd = self.get_parameter('kd').value

        # Allow dynamic updates
        self.add_on_set_parameters_callback(self.param_callback)

        # -------- state --------
        self.encoder = 0.0
        self.setpoint = 0.0

        self.integral = 0.0
        self.prev_error = 0.0

        self.dt = 0.05  # 50 ms loop

        # -------- ROS interfaces --------
        self.create_subscription(Int32, 'enc', self.encoder_cb, 10)
        self.create_subscription(Float64, 'setpoint', self.setpoint_cb, 10)

        self.pub = self.create_publisher(Float64, 'control_effort', 10)

        self.timer = self.create_timer(self.dt, self.compute_control)

        self.get_logger().info(
            f"PID started with kp={self.kp}, ki={self.ki}, kd={self.kd}"
        )

    # -------- parameter callback --------
    def param_callback(self, params):
        for param in params:
            if param.name == 'kp':
                self.kp = param.value
            elif param.name == 'ki':
                self.ki = param.value
            elif param.name == 'kd':
                self.kd = param.value

        self.get_logger().info(
            f"Updated gains: kp={self.kp}, ki={self.ki}, kd={self.kd}"
        )
        return rclpy.parameter.ParameterEventHandler.Result(successful=True)

    # -------- callbacks --------
    def encoder_cb(self, msg: Int32):
        self.encoder = float(msg.data)

    def setpoint_cb(self, msg: Float64):
        self.setpoint = msg.data

# -------- control loop --------
    def compute_control(self):
        if abs(self.setpoint) < 0.001:
            self.integral = 0.0
            self.prev_error = 0.0
            self.encoder = 0.0
            self.pub.publish(Float64(data=0.0))
            return
        # 1. Calculate error based on target speed vs current delta
        error = self.setpoint - self.encoder

        # Proportional
        p = self.kp * error

        # Integral (with simple anti-windup clamp)
        self.integral += error * self.dt
        self.integral = max(-100.0, min(100.0, self.integral))
        i = self.ki * self.integral

        # Derivative
        derivative = (error - self.prev_error) / self.dt
        d = self.kd * derivative

        self.prev_error = error

        effort = p + i + d

        # 2. CORRECTED: Clamp output to allow negative values (-100 to 100)
        # This allows the motor to reverse if it overshoots or if the setpoint is negative
        effort = max(-100.0, min(100.0, effort))

        # 3. IMPORTANT: Reset the encoder count for the next delta window
        # Since encoder_publisher sends "change since last read", we treat this 
        # as a velocity. We must clear it so the next calculation starts fresh.
        self.encoder = 0.0

        msg = Float64()
        msg.data = effort
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SimplePID()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()