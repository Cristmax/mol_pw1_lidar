import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ObstacleDetector(Node):

    def __init__(self):
        super().__init__('obstacle_detector')

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.get_logger().info('Akadályérzékelő elindult.')

    def scan_callback(self, msg):
        center_index = len(msg.ranges) // 2

        start_index = max(0, center_index - 30)
        end_index = min(len(msg.ranges), center_index + 31)

        front_ranges = msg.ranges[start_index:end_index]

        valid_ranges = [
            distance
            for distance in front_ranges
            if msg.range_min <= distance <= msg.range_max
        ]

        if not valid_ranges:
            self.get_logger().warn('Nincs érvényes LIDAR adat.')
            return

        nearest_obstacle = min(valid_ranges)

        if nearest_obstacle < 1.0:
            status = 'AKADÁLY'
        elif nearest_obstacle < 2.0:
            status = 'FIGYELEM'
        else:
            status = 'SZABAD'

        self.get_logger().info(
            f'{status} - Legközelebbi akadály: '
            f'{nearest_obstacle:.2f} m'
        )


def main(args=None):
    rclpy.init(args=args)

    node = ObstacleDetector()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
