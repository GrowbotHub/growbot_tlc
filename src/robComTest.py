#!/usr/bin/env python
import rospy
from growbot_msg.msg import RobArm_cmd
from growbot_msg.msg import RobArm_moving
from growbot_msg.msg import Dispenser_cmd
from growbot_msg.msg import Dispenser_moving


pub_robCmd = None
pub_dispMov = None

def cb_robArm_moving(data):
    rospy.loginfo("Recieved moving : " + str(data.isMoving))


def cb_dispenser_cmd(data):
    rospy.loginfo("Recieved dispenser trigger, waiting a bit")
    rospy.sleep(5)
    msg = Dispenser_moving()
    msg.isMoving = False
    pub_dispMov.publish(msg)
    rospy.loginfo("Dispenser done")


def subscribe():
    rospy.Subscriber("/robArm/moving", RobArm_moving, cb_robArm_moving)
    rospy.Subscriber("/dispenser/cmd", Dispenser_cmd, cb_dispenser_cmd)


def initPublisher():
    global pub_robCmd
    global pub_dispMov
    pub_robCmd = rospy.Publisher('/robArm/cmd', RobArm_cmd, queue_size=10)
    pub_dispMov = rospy.Publisher('/dispenser/moving', Dispenser_moving, queue_size=10)
    

def main():
    subscribe()
    initPublisher()
    rospy.loginfo("robComTest : Running...")
    msg = RobArm_cmd()
    msg.potID = 3
    msg.aero = True
    msg.bringBack = False
    #pub_robCmd.publish(msg)
    #rospy.loginfo("Published")
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        raw_input('Press any key to continue\n')
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

