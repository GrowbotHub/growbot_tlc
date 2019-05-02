#!/usr/bin/env python
import rospy
import dateutil.parser as dup 
from growbot_tlc.msg import Alarm

# Constant
_SCHEDULE_FILE = "/home/ubuntu/catkin_ws/src/growbot_tlc/src/schedule.txt"

_DATE = 0
_CMD_ID = 1
_PARAM1 = 2
_PARAM2 = 3


# Global variable
pub_check = 0
pub_pickUp = 0
schedule = []
scheduleEventPointer = 0 # Correspond to the index of the next schedule entry that will happen


def initPublisher():
	global pub_check
	global pub_pickUp
	pub_check = rospy.Publisher('/alarm/check', Alarm, queue_size=10)
	pub_pickUp = rospy.Publisher('/alarm/pickUp', Alarm, queue_size=10)


def printCurrentTime():
	now = rospy.get_rostime()
	rospy.loginfo("Current time %i %i", now.secs, now.nsecs)


def readSchedule():
	global schedule
	file = open(_SCHEDULE_FILE,"r")
	content = file.read()
	lines = content.split('\n')

	for l in lines:
		if l == "" :
			pass
		elif l[0] == '#':
			pass
		else :
			cmd = l.split(' ')
			date = cmd[_DATE]
			cmdID = cmd[_CMD_ID]
			param1 = int(cmd[_PARAM1])
			param2 = int(cmd[_PARAM2])
			date = dup.parse(date)
			date = int(date.strftime('%s'))

			if len(schedule) > 0 and date < schedule[-1][_DATE] :
				rospy.logwarn("schedule : Out of order entry ignored")
			else :
				schedule.append((date, cmdID, param1, param2))

			
def setTimers():
	global scheduleEventPointer
	now = rospy.get_rostime() 
	for entry in schedule :
		duration = entry[_DATE] - now.secs
		rospy.loginfo(duration)
		if duration < 0:
			rospy.logwarn("schedule : Past entry ignored")
			scheduleEventPointer += 1
		else :
			rospy.Timer(rospy.Duration(duration), timerCallback, oneshot=True)


def timerCallback(data):
	global scheduleEventPointer
	msg_alarm = Alarm()
	msg_alarm.shelfID = schedule[scheduleEventPointer][_PARAM1]
	msg_alarm.potID = schedule[scheduleEventPointer][_PARAM2]

	if schedule[scheduleEventPointer][_CMD_ID] == "PickUp" :
		pub_pickUp.publish(msg_alarm)
	elif schedule[scheduleEventPointer][_CMD_ID] == "Check" :
		pub_check.publish(msg_alarm)
	else :
		rospy.logerr("Unkown command ID in schedule %s",schedule[scheduleEventPointer][_CMD_ID])
	scheduleEventPointer += 1


def main():
	rospy.loginfo("schedule : Runnning...")
	initPublisher()
	readSchedule()
	setTimers()
	rospy.loginfo("schedule : Timer set")
	rospy.spin()


if __name__ == '__main__':
	try:
		rospy.init_node('schedule', anonymous=True)
		main()
	except rospy.ROSInterruptException:
		pass
