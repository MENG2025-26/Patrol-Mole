#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32

import serial


class EncoderPublisher(Node):

    def __init__(self):
        super().__init__('encoder_publisher')

        self.previous_left = 0
        self.previous_right = 0

        # Parameters
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)

        port = self.get_parameter('port').value
        baud = self.get_parameter('baudrate').value

        # Serial setup
        try:
            self.ser = serial.Serial(port, baud, timeout=0.1)
            self.get_logger().info(f"Opened serial port {port} @ {baud}")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            raise

        # Publishers
        self.pub_l = self.create_publisher(Int32, 'enc_l', 10)
        self.pub_r = self.create_publisher(Int32, 'enc_r', 10)

        # Timer (polling loop)
        self.timer = self.create_timer(0.05, self.read_serial)  # 20 Hz

    def read_serial(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if not line:
                return

            parts = line.split(',')
            if len(parts) != 2:
                return

            left = int(parts[0])
            right = int(parts[1])

            # get changes since last read
            delta_left = left - self.previous_left
            delta_right = right - self.previous_right
            
            self.previous_left = left
            self.previous_right = right 
            
            self.pub_l.publish(Int32(data=-delta_left))
            self.pub_r.publish(Int32(data=-delta_right))

        except Exception as e:
            # Avoid spamming logs on occasional bad lines
            self.get_logger().warn(f"Parse error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = EncoderPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()