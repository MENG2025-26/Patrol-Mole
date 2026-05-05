

#!/usr/bin/env python3

# VL53L0X_node.py
# ROS2 Node to interface with VL53L0X Time-of-Flight distance sensor
# This node initializes the sensor, sets its I2C address, and publishes distance readings as sensor_msgs/Range messages.
# It may be necessary to 'pip install vl53l0x --break-system-packages' to get the VL53L0X working, Should be fine as long as you don't have other python packages that depend on it. If you do, you can also just copy the VL53L0X.py file into your package and import it directly.

import rclpy
from rclpy.node import Node
import time

try:
    from gpiozero import OutputDevice
except ImportError:
    OutputDevice = None

# Standard VL53L0X library
import VL53L0X
from sensor_msgs.msg import Range

class VL53L0X_SensorNode(Node):
    def __init__(self):
        super().__init__('VL53L0X_sensor_node')
        
        # 1. Parameters
        self.declare_parameter('i2c_address', 0x29)
        self.declare_parameter('xshut_pin', 20) 
        self.declare_parameter('frame_id', 'wall_sensor_link')

        self.target_address = self.get_parameter('i2c_address').get_parameter_value().integer_value
        self.xshut_pin_num = self.get_parameter('xshut_pin').get_parameter_value().integer_value
        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value

        # 2. Hardware Reset & Address Assignment
        if OutputDevice:
            self.xshut = OutputDevice(self.xshut_pin_num, active_high=True, initial_value=False)
            self.init_hardware()
        else:
            self.get_logger().error("gpiozero not found!")
            return

        # 3. Initialize Sensor
        self.sensor = VL53L0X.VL53L0X(i2c_address=self.target_address)
        try:
            self.sensor.open()
            self.sensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
            self.get_logger().info(f"VL53L0X started at {hex(self.target_address)}")
        except Exception as e:
            self.get_logger().error(f"Failed to start VL53L0X: {e}")

        self.publisher_ = self.create_publisher(Range, 'distance', 10)
        self.timer = self.create_timer(0.1, self.publish_range)

    def init_hardware(self):
        self.xshut.off() # Hold in reset
        time.sleep(0.05)
        self.xshut.on()  # Wake up
        time.sleep(0.05)

        # Temporary object to move from default 0x29 to target
        temp = VL53L0X.VL53L0X(i2c_address=0x29)
        try:
            temp.open()
            temp.change_address(self.target_address)
            temp.close()
        except Exception:
            self.get_logger().warn("Sensor not found at 0x29, might already be assigned.")

    def publish_range(self):
        distance_mm = self.sensor.get_distance()
        if distance_mm > 0:
            msg = Range()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            msg.radiation_type = Range.INFRARED
            msg.field_of_view = 0.436 # Approx 25 degrees
            msg.min_range = 0.03
            msg.max_range = 2.0
            msg.range = float(distance_mm) / 1000.0
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = VL53L0X_SensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.sensor.stop_ranging()
        rclpy.shutdown()

