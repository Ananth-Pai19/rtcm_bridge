#!/usr/bin/env python3
import rclpy as r
from rclpy.node import Node
from rtcm_msgs.msg import Message
from rclpy.qos import QoSProfile, ReliabilityPolicy
import serial

class RtcmPublisher(Node):
    def __init__(self):
        super().__init__("rtcm_publisher_node")

        self.port_name = "/dev/ttyACM0"
        self.baudrate = 115200

        self.qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.pub = self.create_publisher(Message, "/rtcm", self.qos)

        # Initialize the serial communication
        try: 
            self.ser = serial.Serial(self.port_name, self.baudrate, timeout=1)
            self.get_logger().info("Connected to ACM0 (Base station GNSS module)")
        except Exception as e:
            self.get_logger().error(f"Recieved exception: {e}")

        self.timer = self.create_timer(0.1, self.serial_callback)


    def serial_callback(self):
        # Start recieving the messages
        if self.ser.in_waiting > 0:
            # If the buffer is not empty
            raw_data = self.ser.read(self.ser.in_waiting)
        
            rtcm_msg = Message()
            rtcm_msg.header.stamp = self.get_clock().now().to_msg()
            rtcm_msg.header.frame_id = "base"
            rtcm_msg.message = list(raw_data)
            self.pub.publish(rtcm_msg)
            self.get_logger().info(f"Published the RTCM message: {list(raw_data)}")


def main(args=None):
    r.init(args=args)
    node = RtcmPublisher()
    try:
        r.spin(node)
    except KeyboardInterrupt:
        print("YOU DARE KeyboardInterrupt ME!!!") 
    finally:
        r.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()      
    