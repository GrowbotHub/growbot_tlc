#!/usr/bin/env python
import rospy
from growbot_tlc.msg import ImPro_img
from growbot_tlc.msg import ImPro_trig
from growbot_tlc.msg import ImPro_res


# Global variable
pub_res = 0
lastImg = 0
lastShelfID = 0
lastTime = 0


def imgSaver(data):
    global lastImg
    global lastTime
    global lastShelfID
    lastImg = data.img
    lastTime = data.pictureTime
    lastShelfID = data.shelfID


def imgProcessing(data):
    #do image processing
    msg_result = ImPro_res()
    msg_result.result = True
    msg_result.shelfID = lastShelfID
    msg_result.potID = 0
    msg_result.pictureTime = lastTime
    pub_res.publish(msg_result)


def subscribe():
    rospy.Subscriber("/imPro/img", ImPro_img, imgSaver)
    rospy.Subscriber("/imPro/trig", ImPro_trig, imgProcessing)



def initPublisher():
    global pub_res
    pub_res = rospy.Publisher('/imPro/res', ImPro_res, queue_size=10)



def main():
    subscribe()
    initPublisher()
    rospy.loginfo("image_processing : Running...")
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('image_processing', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass

