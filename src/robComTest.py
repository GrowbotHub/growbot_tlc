#!/usr/bin/env python
import rospy
from growbot_msg.msg import RobArm_cmd
from growbot_msg.msg import RobArm_moving

pub_robCmd = None

def cb_robArm_moving(data):
    rospy.loginfo("Recieved moving : " + str(data.isMoving))


def subscribe():
    rospy.Subscriber("/robArm/moving", RobArm_moving, cb_robArm_moving)
    

def initPublisher():
    global pub_robCmd
    pub_robCmd = rospy.Publisher('/robArm/cmd', RobArm_cmd, queue_size=10)
    

def main():
    subscribe()
    initPublisher()
    rospy.loginfo("robComTest : Running...")
    msg = RobArm_cmd()
    msg.potID = 3;
    msg.aero = True;
    msg.bringBack = False;
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        pub_robCmd.publish(msg)
        rospy.loginfo("Published")
        rate.sleep()
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('robComTest', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass

