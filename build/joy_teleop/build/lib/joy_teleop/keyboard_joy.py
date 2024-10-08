import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from pynput import keyboard

class KeyboardJoy(Node):
    def __init__(self):
        super().__init__('keyboard_joy')
        self.publisher_ = self.create_publisher(Joy, 'joy', 10)
        self.timer = self.create_timer(0.00001, self.timer_callback)
        self.joy_msg = Joy()
        self.joy_msg.buttons = [0] * 12  # Assuming 12 buttons
        self.joy_msg.axes = [0.0] * 6  # Assuming 6 axes
        self.shift_pressed = False

        # Start listening to keyboard events
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            if key == keyboard.Key.shift:
                self.shift_pressed = True
            elif key.char == 'w':
                self.joy_msg.axes[1] = 1.0
            elif key.char == 's':
                self.joy_msg.axes[1] = -1.0
            elif key.char == 'a':
                self.joy_msg.axes[2] = 1.0
            elif key.char == 'd':
                self.joy_msg.axes[2] = -1.0
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key == keyboard.Key.shift:
                self.shift_pressed = False
            elif key.char in ['w', 's']:
                self.joy_msg.axes[1] = 0.0
            elif key.char in ['a', 'd']:
                self.joy_msg.axes[2] = 0.0
        except AttributeError:
            pass

    def timer_callback(self):
        self.joy_msg.buttons[4] = 1  # Set deadman switch always to 1
        self.publisher_.publish(self.joy_msg)
        self.get_logger().info(f'Publishing: {self.joy_msg}')

    def destroy_node(self):
        self.listener.stop()  # Stop the keyboard listener
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    keyboard_joy = KeyboardJoy()
    rclpy.spin(keyboard_joy)
    keyboard_joy.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

