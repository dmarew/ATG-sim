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
from atg_sim.srv import *
import time
class TakeActionServer:
    NODE_NAME = "TakeActionServer"

    def __init__(self):
        rospy.init_node(self.NODE_NAME)
        self.bridge = CvBridge()
        rospy.wait_for_service('current_observation')
        self.service = rospy.Service('take_action', TakeAction, self.take_action)
        self.get_current_observation = rospy.ServiceProxy('current_observation', CurrentObservation)
        self.action_pub = rospy.Publisher("/joint_states", JointState, queue_size=10)

    def take_action(self, request):
        print('taking action ', request.angle.data)
        joint_action = JointState()
        joint_action.header = Header()
        joint_action.header.stamp = rospy.Time.now()
        joint_action.name = ['joint1']
        joint_action.position = [request.angle.data]
        joint_action.velocity = [0.01]
        joint_action.effort = []
        self.action_pub.publish(joint_action)
        time.sleep(2)
        return TakeActionResponse(self.get_current_observation().img)

if __name__=="__main__":
	tas = TakeActionServer()
	try:
		rospy.spin()
	except:
		rospy.loginfo("error!!")
