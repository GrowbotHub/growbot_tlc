#!/usr/bin/env python
import rospy
from growbot_msg.msg import Alarm
from growbot_msg.msg import RobArm_cmd
from growbot_msg.msg import RobArm_moving
from growbot_msg.msg import Wheel_target
from growbot_msg.msg import Wheel_moving
from growbot_msg.msg import ImPro_trig
from growbot_msg.msg import ImPro_res
from growbot_msg.msg import User_cmd
from growbot_msg.srv import ImPro_doImPro
import constants as cst

# Global variable
pub_robCmd = 0
pub_wheelTarget = 0
pub_imProTrig = 0

lastLsShelf = cst._SHELFID_LS1
lastVeggiShelf = cst._SHELFID_SALAD
lastBringBack = False

lastCmdDone = True

lastPotID = [0, 0, 0, 0]

def handleImgProcessing():
    try:
        rospy.wait_for_service('/imPro/doImPro')
        res = rospy.ServiceProxy('/imPro/doImPro', ImPro_doImPro)
        return res()
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s", e)
        rospy.logwarn("Returned default image path")


def ripnessCheck():
    #rob arm go safe
    #wait done moving
    #for all shleves :
    #   move to shelf
    #   wait for done moving
    #   take pic (that is a problem... -> make a ROS node on RPi ?)
    rospy.loginfo("main : Ripness check routine triggered")
    handleImgProcessing()


def imProResSaver(data):
    pass



def showLunarSoil():
    global lastCmdDone
    global lastLsShelf
    global lastBringBack
    global lastPotID

    lastCmdDone = False

    if cst._WHEEL_CONNECTED :
        newTarget = Wheel_target()
        if lastLsShelf == cst._SHELFID_LS1 :
            lastLsShelf = cst._SHELFID_LS2
            newTarget.target = cst._BASEPOS_LS2 + cst._WORK_OFFSET
        elif lastLsShelf == cst._SHELFID_LS2 :
            lastLsShelf = cst._SHELFID_LS1
            newTarget.target = cst._BASEPOS_LS1 + cst._WORK_OFFSET

        pub_wheelTarget.publish(newTarget)
        msg_done = rospy.wait_for_message("/wheel/done", Wheel_moving)
        while msg_done.isMoving == True :
            rospy.logwarn("Revieced a isMoving == True message, expected False. Waiting for next isMoving message.")
            msg_done = rospy.wait_for_message("/wheel/done", Wheel_moving)

    # Send command to RobArm
    # Wait for it beeing done
    if cst._ROBARM_CONNECTED:
        robCmd = RobArm_cmd()
        robCmd.potID = lastPotID[lastLsShelf]
        robCmd.aero = False
        lastBringBack = not lastBringBack
        robCmd.bringBack = lastBringBack
        if lastBringBack :
            lastPotID[lastLsShelf] += 1
            if lastPotID[lastLsShelf] >= cst._TOT_POT_NBR :
                rospy.logwarn("Out of pots ! Restarting at potID = 0")
                lastPotID[lastLsShelf] = 0

        pub_robCmd.publish(robCmd)
        msg_done = rospy.wait_for_message("/robArm/done", RobArm_moving)
        while msg_done.isMoving == True :
            rospy.logwarn("RobArm : Revieced a isMoving == True message, expected False. Waiting for next isMoving message.")
            msg_done = rospy.wait_for_message("/robArm/done", RobArm_moving)

    lastCmdDone = True
    rospy.loginfo("Done handeling LS")


def harvest():
    global lastCmdDone
    global lastVeggiShelf
    global lastPotID

    lastCmdDone = False

    if cst._WHEEL_CONNECTED :
        newTarget = Wheel_target()
        if lastVeggiShelf == cst._SHELFID_SALAD :
            lastVeggiShelf = cst._SHELFID_RADISH
            newTarget.target = cst._BASEPOS_RADISH + cst._WORK_OFFSET
        elif lastVeggiShelf == cst._SHELFID_RADISH :
            lastVeggiShelf = cst._SHELFID_SALAD
            newTarget.target = cst._BASEPOS_SALAD + cst._WORK_OFFSET

        pub_wheelTarget.publish(newTarget)
        msg_done = rospy.wait_for_message("/wheel/done", Wheel_moving)
        while msg_done.isMoving == True :
            rospy.logwarn("Wheel : Revieced a isMoving == True message, expected False. Waiting for next isMoving message.")
            msg_done = rospy.wait_for_message("/wheel/done", Wheel_moving)

    # Send command to RobArm
    # Wait for it beeing done
    if cst._ROBARM_CONNECTED :
        robCmd = RobArm_cmd()
        robCmd.potID = lastPotID[lastVeggiShelf]
        lastPotID[lastVeggiShelf] += 1
        if lastPotID[lastVeggiShelf] >= cst._TOT_POT_NBR :
            rospy.logwarn("Out of pots ! Restarting at potID = 0")
            lastPotID[lastVeggiShelf] = 0
        robCmd.aero = True
        robCmd.bringBack = False
        pub_robCmd.publish(robCmd)
        msg_done = rospy.wait_for_message("/robArm/done", RobArm_moving)
        while msg_done.isMoving == True :
            rospy.logwarn("RobArm : Revieced a isMoving == True message, expected False. Waiting for next isMoving message.")
            msg_done = rospy.wait_for_message("/robArm/done", RobArm_moving)

    lastCmdDone = True
    rospy.loginfo("Done harvesting")



def usrCmd(data):
    rospy.loginfo("Usr command recieved")
    if not lastCmdDone :
        rospy.logwarn("Last user command still executing, new command ignored.")
        return
    
    if data.cmdID == cst._CMDID_LS : # show lunar soil
        showLunarSoil()
    elif data.cmdID == cst._CMDID_HARVEST :
        harvest()
    elif data.cmdID == cst._CMDIF_RIPCHECK :
        ripnessCheck()
    else :
        rospy.logerr("Unkown user command recieved")



def subscribe():
    rospy.Subscriber("/alarm/check", Alarm, ripnessCheck)
    #rospy.Subscriber("/alarm/pickUp", Alarm, harvest)
    rospy.Subscriber("/imPro/res", ImPro_res, imProResSaver)
    #rospy.Subscriber("/wheel/done", Wheel_moving, wheelStateUpdate)
    #rospy.Subscriber("/robArm/moving", RobArm_moving, robArmStateUpdate)
    rospy.Subscriber('/usr/cmd', User_cmd, usrCmd)

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

