#!/usr/bin/env python

import rospy
from growbot_tlc.srv import *

def callServ():
    rospy.wait_for_service('/imPro/doImPro')
    try:
        doImPro = rospy.ServiceProxy('/imPro/doImPro', ImPro_doImPro)
        print(doImPro(1))
    except rospy.ServiceException, e:
        print("Service call failed: %s", e)

if __name__ == "__main__":
    rospy.loginfo("Running...")
    callServ()
    rospy.loginfo("Done")

    