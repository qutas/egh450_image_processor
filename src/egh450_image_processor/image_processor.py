#!/usr/bin/env python

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

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
		(rows,cols,channels) = cv_image.shape
		if cols > 20 and rows > 20 :
			# Draw circle at position (50,50), with diameter (10), bgr value (0,0,255), and thickness (2)
			cv2.circle(cv_image, (cols/2,rows/2), 100, (0, 0, 255), 10)
		# ===================

		#Convert CV image to ROS image and publish
		try:
			self.pub_img.publish( self.bridge.cv2_to_imgmsg( cv_image, "bgr8" ) )
		except CvBridgeError as e:
			print(e)
