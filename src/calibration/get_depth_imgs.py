# -*- coding: utf-8 -*-
# @File    : get_depth_imgs.py
# @Time    : 18-7-10 下午3:25
# @Author  : Jee
# @Email   : jee_shao@163.com

import rospy
import numpy as np
from sensor_msgs.msg import  Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


def callback(data):
        try:
            depth_image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        # print(depth_image.shape)   #1080*1920
        depth_image = depth_image.copy()
        depth_min = np.amin(depth_image)
        depth_max = np.amax(depth_image)
        factor = 255.0 / float(depth_max - depth_min)
        depth_image = np.minimum(np.maximum(depth_image - depth_min, 0) * factor, 255.0)
        depth_image = depth_image.astype(np.uint8)
        cv2.imshow("Depth Image", depth_image)
        if cv2.waitKey(1) & 0xFF == 0x22:
            cv2.imwrite('depth.png',depth_image)
        cv2.waitKey(5)

def kinect2_display():
    rospy.init_node("kinect2_color", anonymous=True)
    # make a video_object and init the video object
    global count, bridge
    bridge = CvBridge()
    rospy.Subscriber('/kinect2/hd/image_depth_rect', Image, callback)
    rospy.spin()


if __name__ == '__main__':
    kinect2_display()

