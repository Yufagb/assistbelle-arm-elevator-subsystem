# video_publisher.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import subprocess
import time

class VideoPublisher(Node):
    def __init__(self):
        super().__init__('video_publisher')
        self.declare_parameter('fps', 1)
        self.fps = float(self.get_parameter('fps').value)
        self.lastCaptureTime = time.time()
        # Re-activar autofocus continuo de la Logitech Brio
        subprocess.run([
            'v4l2-ctl','-d',f'/dev/video2',
            '-c','focus_automatic_continuous=1'
        ], check=True)
        self.pub = self.create_publisher(Image, 'camera/image', 1)
        self.bridge = CvBridge()

        # Abre la cámara con V4L2 y MJPG
        self.cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not self.cap.isOpened():
            self.get_logger().error('No se pudo abrir la cámara')
            return

        timer_period = 1.0 / self.fps
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('No se pudo leer frame')
            return
        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(msg)
        ctime = time.time()
        realfps = 1.0/(ctime-self.lastCaptureTime)
        self.lastCaptureTime = ctime
        self.get_logger().info(f'fps:{realfps}')
def main(args=None):
    rclpy.init(args=args)
    node = VideoPublisher()
    rclpy.spin(node)
    node.cap.release()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
