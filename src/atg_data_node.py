#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import os
import numpy as np
import rospy
import cv2
from std_msgs.msg import String, Header
from sensor_msgs.msg import Image, JointState
from cv_bridge import CvBridge, CvBridgeError

class AspectTransition:

    def __init__(self):

        self.action_pub = rospy.Publisher("/joint_states", JointState, queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/rrbot/camera1/image_raw",Image,self.callback)
        self.data_path = rospy.get_param("~data_path", '.')

        self.observation_count = 0
        self.action_count = 0

    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            write_loc = 'observation_' + str(self.observation_count) + '.png'
            rospy.logwarn(write_loc)
            rospy.logwarn(self.data_path )

            cv2.imwrite(write_loc , cv_image)
        except CvBridgeError as e:
            print(e)


        self.observation_count += 1
        cv2.imshow("Image window", cv_image)
        cv2.waitKey(1000)
        try:
            action = JointState()
            action.header = Header()
            action.header.stamp = rospy.Time.now()
            action.name = ['joint1']
            action_param = np.random.randint(15)*0.1
            action.position = [action_param]
            action.velocity = [0.01]
            action.effort = []
            self.action_pub.publish(action)
            print(action_param)


        except CvBridgeError as e:
            print(e)

def main(args):
    at = AspectTransition()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
