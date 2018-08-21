#!/usr/bin/env python

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# will need to change the location to your own environment
sign_cascade = cv2.CascadeClassifier('/home/kyle/catkin_ws/src/egh450_image_processor/data/cascade.xml')

class ImageProcessor():
	def __init__(self):
		#Set up the CV Bridge
		self.bridge = CvBridge()

		# Set up the subscriber
		self.sub_img = rospy.Subscriber('~image_input', Image, self.callback_img)
		self.pub_img = rospy.Publisher('~image_output', Image, queue_size=1)

	def shutdown(self):
		# Unregister anything that needs it here
		self.sub_img.unregister()

	def callback_img(self, msg_in):
		#Convert ROS image to CV image
		try:
			cv_image = self.bridge.imgmsg_to_cv2( msg_in, "bgr8" )
		except CvBridgeError as e:
			print(e)

		# ===================
		# Do processing here!
		# ===================
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		
		sign = sign_cascade.detectMultiScale(gray, 1.01, 1, minSize=(100,100))
		
		for (x,y,w,h) in sign:
			cv2.rectangle(cv_image,(x,y),(x+w,y+h),(255,0,0),2)
		
		# ===================

		#Convert CV image to ROS image and publish
		try:
			self.pub_img.publish( self.bridge.cv2_to_imgmsg( cv_image, "bgr8" ) )
		except CvBridgeError as e:
			print(e)
