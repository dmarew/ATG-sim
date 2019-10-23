#!/usr/bin/env python

import sys
import rospy
from atg_sim.srv import *

if __name__ == "__main__":
    rospy.wait_for_service('current_observation')
    get_current_observation = rospy.ServiceProxy('current_observation', CurrentObservation)
    response = get_current_observation()
    print(response.img.height)
