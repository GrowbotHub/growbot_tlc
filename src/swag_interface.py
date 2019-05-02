#!/usr/bin/env python

import rospy
from growbot_tlc.msg import Meas_sensor
from growbot_tlc.msg import ImPro_img

# Constants
_RATE = 10 #Hz

# Gloabal variable
lastAirTemp = 0.
lastWaterTemp = 0.
lastHumidity = 0.
lastMearmentTime = 0
lastImage = 0

pub_airTemp = 0
pub_waterTemp = 0
pub_humidity = 0
pub_img = 0

def getMeasurements():
    global lastAirTemp
    global lastWaterTemp
    global lastHumidity
    global lastMearmentTime
    lastAirTemp = 1.
    lastWaterTemp = 1.
    lastHumidity = 1.
    lastMearmentTime = 1.


def getImage():
    pass

def initPublisher():
    global pub_airTemp
    global pub_waterTemp
    global pub_humidity
    global pub_img
    pub_airTemp = rospy.Publisher('/meas/airTemp', Meas_sensor, queue_size=10)
    pub_waterTemp = rospy.Publisher('/meas/waterTemp', Meas_sensor, queue_size=10)
    pub_humidity = rospy.Publisher('/meas/humidity', Meas_sensor, queue_size=10)
    pub_img = rospy.Publisher('/imPro/img', ImPro_img, queue_size=10)


def publishMeasurements():
    #airTemp    
    msg_airTemp = Meas_sensor()
    msg_airTemp.value = lastAirTemp
    msg_airTemp.measurmentTime.secs = lastMearmentTime
    msg_airTemp.measurmentTime.nsecs = 0
    pub_airTemp.publish(msg_airTemp)

    #waterTemp    
    msg_waterTemp = Meas_sensor()
    msg_waterTemp.value = lastWaterTemp
    msg_waterTemp.measurmentTime.secs = lastMearmentTime
    msg_waterTemp.measurmentTime.nsecs = 0
    pub_waterTemp.publish(msg_waterTemp)

    #humidity    
    msg_humidity = Meas_sensor()
    msg_humidity.value = lastHumidity
    msg_humidity.measurmentTime.secs = lastMearmentTime
    msg_humidity.measurmentTime.nsecs = 0
    pub_airTemp.publish(msg_humidity)

def publishImage():
    # how do we know the shlef ID of pic ?
    pass


def main():
    initPublisher()
    rate = rospy.Rate(_RATE)
    rospy.loginfo("swag_interface : Running...")
    while not rospy.is_shutdown():
        getMeasurements()
        publishMeasurements()
        getImage()
        publishImage()
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('swag_interface', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass
