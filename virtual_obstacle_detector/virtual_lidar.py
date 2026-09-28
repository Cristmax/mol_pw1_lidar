import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class VirtualLidar(Node):

    def __init__(self):
        super().__init__('virtual_lidar')

        self.publisher = self.create_publisher(
            LaserScan,
            '/scan',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.publish_scan
        )

        self.get_logger().info('Virtual LIDAR elindult.')

    def publish_scan(self):
        scan = LaserScan()

        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = 'laser'

        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = math.radians(1.0)

        scan.range_min = 0.1
        scan.range_max = 10.0

        number_of_rays = 361

        scan.ranges = [5.0] * number_of_rays

        # Virtuális akadály 2 méterre, a robot előtt.
        center_index = 180

        for i in range(center_index - 10, center_index + 11):
            scan.ranges[i] = 2.0

        self.publisher.publish(scan)


def main(args=None):
    rclpy.init(args=args)

    node = VirtualLidar()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
