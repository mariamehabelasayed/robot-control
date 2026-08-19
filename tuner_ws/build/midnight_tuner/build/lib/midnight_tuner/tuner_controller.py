import sys
import select
import termios
import tty
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Color
from std_msgs.msg import String

# Safe terminal setup so the launch file doesn't crash on startup
try:
    settings = termios.tcgetattr(sys.stdin)
except termios.error:
    settings = None

def get_key():
    if settings is None:
        return ''
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    except Exception:
        return ''

class MidnightTunerController(Node):
    def __init__(self):
        super().__init__('midnight_tuner_controller')

        # 4. Parameters for runtime topic configuration
        self.declare_parameter('cmd_vel_topic', '/turtle1/cmd_vel')
        self.declare_parameter('color_sensor_topic', '/turtle1/color_sensor')
        self.declare_parameter('dominant_color_topic', '/dominant_color')

        cmd_topic = self.get_parameter('cmd_vel_topic').get_parameter_value().string_value
        sensor_topic = self.get_parameter('color_sensor_topic').get_parameter_value().string_value
        dominant_topic = self.get_parameter('dominant_color_topic').get_parameter_value().string_value

        # 2. Movement Publisher (Non-holonomic: linear.x & angular.z only)
        self.publisher_cmd = self.create_publisher(Twist, cmd_topic, 10)

        # 3. Perception Subscriber
        self.subscription_color = self.create_subscription(
            Color,
            sensor_topic,
            self.color_callback,
            10
        )

        # 3. Action 2: Custom Topic Publisher for Major Color
        self.publisher_dominant = self.create_publisher(String, dominant_topic, 10)

        # Timer for reading keyboard inputs and publishing velocities (0.1s interval)
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info("Midnight Tuner Gang online! Use W/S to throttle, A/D to steer.")

    def control_loop(self):
        key = get_key()
        twist = Twist()

        # Non-holonomic movement mapping
        if key == 'w':
            twist.linear.x = 2.0
            twist.angular.z = 0.0
        elif key == 's':
            twist.linear.x = -2.0
            twist.angular.z = 0.0
        elif key == 'a':
            twist.linear.x = 1.0
            twist.angular.z = 2.0
        elif key == 'd':
            twist.linear.x = 1.0
            twist.angular.z = -2.0
        elif key == '\x03':  # Ctrl+C termination check
            rclpy.shutdown()
        else:
            # Halt if no valid key is pressed
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        self.publisher_cmd.publish(twist)

    def color_callback(self, msg: Color):
        r, g, b = msg.r, msg.g, msg.b

        # Determine major/dominant color channel
        if r >= g and r >= b:
            dominant = "RED"
        elif g >= r and g >= b:
            dominant = "GREEN"
        else:
            dominant = "BLUE"

        # Action 1: Standard ROS2 logging
        self.get_logger().info(f"Neon Underglow Detected -> R:{r} G:{g} B:{b} | Major Color: {dominant}")

        # Action 2: Publish major color string
        color_msg = String()
        color_msg.data = dominant
        self.publisher_dominant.publish(color_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MidnightTunerController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()