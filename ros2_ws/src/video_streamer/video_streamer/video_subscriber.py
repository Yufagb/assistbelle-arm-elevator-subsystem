import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VideoSubscriber(Node):
    def __init__(self):
        super().__init__('video_subscriber')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(
            Image, 'camera/image', self.listener_callback, 10)

        # Crear la ventana una sola vez
        cv2.namedWindow('Vídeo remoto', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Vídeo remoto', 640, 480)

    def listener_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # Actualiza la ventana existente
        cv2.imshow('Vídeo remoto', frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = VideoSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
