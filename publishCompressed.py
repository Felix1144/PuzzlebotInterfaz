#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2

def image_publisher():
    rospy.init_node('image_publisher', anonymous=True)
    pub = rospy.Publisher('image_topic/compressed', CompressedImage, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz
    bridge = CvBridge()
    cap = cv2.VideoCapture(0)  # Captura de la cámara

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            # Convertir la imagen a formato JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, jpeg_image = cv2.imencode('.jpg', frame)

            # Crear un mensaje de imagen comprimida y publicarlo
            compressed_image_msg = CompressedImage()
            compressed_image_msg.header.stamp = rospy.Time.now()
            compressed_image_msg.format = "jpeg"
            compressed_image_msg.data = jpeg_image.tobytes()
            pub.publish(compressed_image_msg)
            rate.sleep()

    cap.release()

if __name__ == '__main__':
    try:
        image_publisher()
    except rospy.ROSInterruptException:
        pass
