import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

class JoyOverrideNode(Node):

    def __init__(self):
        super().__init__('joy_override_node')

        # Publisher for the overridden joy messages
        self.publisher_override = self.create_publisher(Joy, '/joy_override', 10)

        # Publisher for the original joy messages
        self.publisher = self.create_publisher(Joy, '/joy', 10)

        # Subscribe to the /joy topic
        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10
        )

    def joy_callback(self, joy_msg):
        # Check if the deadman button (button[4]) is 0, and override it
        if joy_msg.buttons[4] == 0:
            self.get_logger().info('Deadman button is not pressed, overriding it.')
            joy_msg.buttons[4] = 1

        # Log the updated message for debugging
        self.get_logger().info(f'Updated /joy message: {joy_msg}')

        # Publish the modified message to the /joy_override topic
        self.publisher_override.publish(joy_msg)

        # Also publish back to the /joy topic if you want the original topic to reflect changes
        self.publisher.publish(joy_msg)

def main(args=None):
    rclpy.init(args=args)

    node = JoyOverrideNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

