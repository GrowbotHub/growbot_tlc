#!/usr/bin/env python
import rospy
from growbot_tlc.msg import Alarm
from growbot_tlc.msg import RobArm_cmd
from growbot_tlc.msg import RobArm_moving
from growbot_tlc.msg import Wheel_target
from growbot_tlc.msg import Wheel_moving
from growbot_tlc.msg import ImPro_trig
from growbot_tlc.msg import ImPro_res

# Global variable
pub_robCmd = 0
pub_wheelTarget = 0
pub_imProTrig = 0


def ripnessCheck(data):
    #rob arm go safe
    #wait done moving
    #for all shleves :
    #   move to shelf
    #   wait for done moving
    #   take pic (that is a problem... -> make a ROS node on RPi ?)
    rospy.loginfo("main : Ripness check routine triggered")
    pass


def pickingUp(data):
    #rob arm go safe
    #wait done moving
    #move to shelf
    #wait done moving
    #rob arm pick up 
    #rob arm go safe
    pass


def imProResSaver(data):
    pass


def wheelStateUpdate(data):
    pass


def robArmStateUpdate(data):
    pass

def subscribe():
    rospy.Subscriber("/alarm/check", Alarm, ripnessCheck)
    rospy.Subscriber("/alarm/pickUp", Alarm, pickingUp)
    rospy.Subscriber("/imPro/res", ImPro_res, imProResSaver)
    rospy.Subscriber("/wheel/moving", Wheel_moving, wheelStateUpdate)
    rospy.Subscriber("/robArm/moving", RobArm_moving, robArmStateUpdate)


def initPublisher():
    global pub_robCmd
    global pub_wheelTarget
    global pub_imProTrig
    pub_robCmd = rospy.Publisher('/robArm/cmd', RobArm_cmd, queue_size=10)
    pub_wheelTarget = rospy.Publisher('/wheel/target', Wheel_target, queue_size=10)
    pub_imProTrig = rospy.Publisher('/imPro/trig', ImPro_trig, queue_size=10)


def main():
    subscribe()
    initPublisher()
    rospy.loginfo("main : Running...")
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('main', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass

