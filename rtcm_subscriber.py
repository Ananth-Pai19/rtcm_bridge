#!/usr/bin/env python3 
import rclpy as r
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rtcm_msgs.msg import Message
import serial


class RtcmSubscriber(Node):
    def __init__(self):
        super().__init__("rtcm_subscriber_node")

        self.qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.subscriber = self.create_subscription(Message, "/rtcm", self.rtcm_callback, self.qos)

        # Make this robust later
        self.port_name = "/dev/ttyACM0"
        self.baudrate = 115200

        try:
            self.ser = serial.Serial(self.port_name, self.baudrate, timeout=1)
            self.get_logger().info("Connected to RTK GNSS module on rover!")
        except Exception as e:
            self.get_logger().error(f"Exception occured: {e}")

    
    def rtcm_callback(self, message: Message):
        if message is not None:
            try:
                rtcm_data = bytes(message.message)
                if self.ser.is_open and self.ser.out_waiting == 0:
                    self.ser.write(rtcm_data)
                    self.get_logger().info(f"Sent {len(rtcm_data)} to the Rover GNSS module!")
            except Exception as e:
                self.get_logger().error(f"Exception: {e}")

            
def main(args=None):
    r.init(args=args)
    node = RtcmSubscriber()
    try:
        r.spin(node)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        r.shutdown()
        node.destroy_node()        

    
if __name__ == "__main__":
    main()