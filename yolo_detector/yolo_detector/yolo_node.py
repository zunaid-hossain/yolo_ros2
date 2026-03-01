#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from ultralytics import YOLO
import cv2
import numpy as np
import os
from ament_index_python.packages import get_package_share_directory

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')

        # Find model path in your package
        package_share_directory = get_package_share_directory('yolo_detector')
        model_path = os.path.join(package_share_directory, 'models', 'custom_yolo.onnx')
        self.get_logger().info(f"Loading YOLO ONNX model from: {model_path}")

        # Initialize YOLO model
        self.model = YOLO(model_path, task='detect')
        self.get_logger().info("Model loaded")

        # Subscribe to Mobile Sensor Bridge camera topic
        self.subscription = self.create_subscription(
            CompressedImage,
            '/camera/image_raw/compressed',
            self.listener_callback,
            10
        )

        # Publisher for annotated images
        self.publisher = self.create_publisher(
            CompressedImage,
            '/yolo/annotated_image/compressed',
            10
        )

        self.get_logger().info('YOLO Detector node is ready!')

    def listener_callback(self, msg):
        try:
            # Decode compressed image
            np_arr = np.frombuffer(msg.data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Run YOLO inference
            results = self.model.predict(source=img, conf=0.5, verbose=False)
            annotated_image = results[0].plot()

            # Compress annotated image
            _, encimg = cv2.imencode('.jpg', annotated_image, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

            out_msg = CompressedImage()
            out_msg.header = msg.header
            out_msg.format = "jpeg"
            out_msg.data = encimg.tobytes()

            # Publish annotated image
            self.publisher.publish(out_msg)
            self.get_logger().info('Published annotated image')

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = YoloDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

