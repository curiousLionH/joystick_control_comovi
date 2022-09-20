#! /usr/bin/env python

'''
subscribe joystick command and publish control command
          0  1  2  3  4   5   6   7   8     9      10    11
button : [A, B, X, Y, LB, RB, LT, RT, BACK, START, joyL, joyR]

driving mode :  Auto Drive      0
                Emergency Stop  1
                Manual Drive    2
                
written by Joohyun Lee
'''

from socket import inet_ntoa
import numpy as np
import time
import rospy
import roslib
import subprocess
import operator as op
import ast
import traceback
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from joy_control.msg import joy_msg, driving_mode
import sys
import signal

class JoyControl:
    def __init__(self):
        self.joy = None
        self.joy2 = None

        self.AutoDrivingMode = False
        self.EmergencyStop = True    # default = Emergency Stop
        self.ManualDrivingMode = False 

        # self.move_cmd = Twist()   
        self.move_cmd = joy_msg()   # Left Wheel Speed, Right Wheel Speed
        self.driving_mode = driving_mode()
        self.driving_mode.mode = 1      # default = Emergency Stop
        self.prev_driving_mode = 1

        self.joyL = [0.0,0.0]
        self.joyR = [0.0,0.0]
        self.arrowkey = [0.0,0.0]   # rotation(left, right), move without steering(straight, back)
        
        # publisher
        # self.control_pub = rospy.Publisher('control_command', Twist, queue_size=1)
        self.control_pub = rospy.Publisher('control_command', joy_msg, queue_size=1)
        self.dirving_mode_pub = rospy.Publisher('driving_mode', driving_mode, queue_size=1)

        # subscriber
        self.joy_sub = rospy.Subscriber("joy", Joy, self.callback,
            queue_size=rospy.get_param("~queue_size", None))

        self.rate = rospy.Rate(20)

    def callback(self, msg):
        self.joyL = [0.0,0.0]
        self.joyR = [0.0,0.0]
        self.arrowkey = [0.0,0.0]
        self.driving_mode.mode = self.prev_driving_mode

        self.joy = msg.buttons
        self.joy2 = msg.axes

        if self.joy[1] == 1:
            rospy.loginfo("Emergency Stop!!!")
            self.EmergencyStop = True
            self.AutoDrivingMode = False
            self.ManualDrivingMode = False
            self.driving_mode.mode = 1
        elif self.joy[2] == 1:
            rospy.loginfo("Manual Driving Mode")
            self.EmergencyStop = False
            self.AutoDrivingMode = False
            self.ManualDrivingMode = True
            self.driving_mode.mode = 2
        elif self.joy[0] == 1:
            rospy.loginfo("Auto Driving Mode")
            self.EmergencyStop = False
            self.AutoDrivingMode = True
            self.ManualDrivingMode = False
            self.driving_mode.mode = 0

        if self.joy2[6] != 0 or self.joy2[7] != 0:      # control with arrow key
            self.arrowkey[0] = self.joy2[6]*(-1)
            self.arrowkey[1] = (self.joy2[7])
        else:                                           # control with joystick
            self.joyL[0] = self.joy2[0]*(-1)
            self.joyL[1] = self.joy2[1]
            self.joyR[0] = self.joy2[3]*(-1)
            self.joyR[1] = self.joy2[4]

    def main(self):
        while rospy.is_shutdown() == False:
            if self.arrowkey[0] != 0:       # arrow key control - simple straight, back
                self.move_cmd.left_wheel = self.arrowkey[0]
                self.move_cmd.right_wheel = self.arrowkey[0]*(-1)
            elif self.arrowkey[1] != 0:     # arrow key control - rotate
                self.move_cmd.left_wheel = self.arrowkey[1]
                self.move_cmd.right_wheel = self.arrowkey[1]
            else:
                self.move_cmd.left_wheel = self.joyL[1]
                self.move_cmd.right_wheel = self.joyR[1]  

            # rospy.loginfo("move command : %f %f\n", self.move_cmd.left_wheel, self.move_cmd.right_wheel)  

            # Publish
            self.move_cmd.time = rospy.Time.now()
            self.driving_mode.time = rospy.Time.now()
            self.control_pub.publish(self.move_cmd)
            self.dirving_mode_pub.publish(self.driving_mode)
            self.prev_driving_mode = self.driving_mode.mode

if __name__ == '__main__':
    try:
        rospy.init_node('joy_pub')
        JoyControl = JoyControl()
        JoyControl.main()
    except rospy.ROSInterruptException:
        pass