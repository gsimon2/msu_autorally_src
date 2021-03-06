#!/usr/bin/env python
#
# Speed Signal Publisher
#
#	This creates a ROS publisher that will post speed commands (as m/s) to the constant speed controller
#
# GAS 2018-06-28

import rospy
import argparse
import time
import math

from std_msgs.msg import Float64


class SpeedSignalPublisherNode():
	def __init__(self, cmd_args):
		
		# Init Node
		self.node_name = 'speed_signal_publisher_node'
		rospy.init_node(self.node_name, anonymous=False)
		
		# Register shutdown hook
		rospy.on_shutdown(self.on_shutdown)
		
		# Write command line arguments into class variables
		self.debug = (cmd_args.debug or rospy.get_param('/DEBUG',False))
		
		self.running = True
		self.speed_pub = rospy.Publisher('/constantSpeedController/speedCommand', Float64, queue_size=10)
		self.sleep_rate = rospy.Rate(10) # Hz
		
		# Rospy returns 0 if the call to get_time() does not receive a value from /clock before the timeout period
		#	This happens commonly on slower than real time simulation, thus loop until non-zero value is returned
		self.start_time = 0
		while self.start_time == 0:
			self.start_time = rospy.get_time()

		
		while self.running:
			#self.speed_pub.publish(self.basic_double_ramp_speed_function())
			self.speed_pub.publish(self.basic_double_ramp_speed_function())
			self.sleep_rate.sleep()
			
	
	# Used for the tuning experiments where the stateEstimator is used
	def SE_basic_double_ramp_speed_function(self):
		current_time = 0
		while current_time == 0:
			current_time = rospy.get_time()
		time = (current_time - self.start_time)
		
		goal_speed = 0
		
		if time < 7:
			goal_speed = 3
		elif 7 <= time < 10:
			goal_speed = 0
		else:
			time = time - 10
			
			if 0 <= time < 5:
				goal_speed = time
			elif 5 <= time < 10:
				goal_speed = 5
			elif 10 <= time < 15:
				goal_speed = -time + 15
			elif 15 <= time < 20:
				goal_speed = (time-15)
			elif 20 <= time < 25:
				goal_speed = 5
			elif 25 <= time < 30:
				goal_speed = -time + 30
			else:
				self.running = False
			
		#print('Time: {} \t Goal Speed: {}'.format(time, goal_speed))
		return goal_speed	
	
	
	
	# Testing speed signal 4
	def tester_signal4(self):
		current_time = 0
		while current_time == 0:
			current_time = rospy.get_time()
		time = (current_time - self.start_time)
		
		goal_speed = 0
		
		if time <= 40:
			goal_speed = int(time)/3
		else:
			self.running = False
		return goal_speed
	
	# Testing speed signal 3
	def tester_signal3(self):
		current_time = 0
		while current_time == 0:
			current_time = rospy.get_time()
		time = (current_time - self.start_time)
		
		goal_speed = 0
		
		if time <= 20:
			goal_speed = int(time)
		else:
			self.running = False
		return goal_speed
	
	# Testing speed signal 2
	def tester_signal2(self):
		current_time = 0
		while current_time == 0:
			current_time = rospy.get_time()
		time = (current_time - self.start_time)
		
		goal_speed = 0
		
		if time <= 25:
			goal_speed = 4 * math.sin(time/2 - math.pi / 2) + 4
		else:
			self.running = False
		return goal_speed
	
	
	# Testing speed signal 1
	def tester_signal(self):
		current_time = 0
		while current_time == 0:
			current_time = rospy.get_time()
		time = (current_time - self.start_time)
		
		#print('time: {}'.format(time))
		
		goal_speed = 0
		
		# 1
		if 0 <= time < 5:
			goal_speed = 2 * time
		# 2
		elif 5 <= time < 7.5:
			goal_speed = -(5/2.5) * (time - 5) + 10
		# 3
		elif 7.5 <= time < 10:
			goal_speed = 5
		#4
		elif 10 <= time < 17.5:
			goal_speed = (10/7.5) * (time - 10) + 5
		#5
		elif 17.5 <= time < 20:
			goal_speed = -(5/2.5) * (time - 17.5) + 15
		#6
		elif 20 <= time < 25:
			goal_speed = 10
		#7
		elif 25 <= time < 30:
			goal_speed = -(10/5) * (time - 25) + 10
		#8
		elif 30 <= time < 35:
			goal_speed = (15/5)*(time-30)
		#9
		elif 35 <= time < 40:
			goal_speed = -(15/5)*(time-35)+15
		else:
			self.running = False
			
		return goal_speed
		
		
		
	# Used for the tuning experiments
	def basic_double_ramp_speed_function(self):
		current_time = 0
		while current_time == 0:
			current_time = rospy.get_time()
		time = (current_time - self.start_time)
		
		goal_speed = 0
		
		if 0 <= time < 5:
			goal_speed = time
		elif 5 <= time < 10:
			goal_speed = 5
		elif 10 <= time < 15:
			goal_speed = -time + 15
		elif 15 <= time < 20:
			goal_speed = (time-15)
		elif 20 <= time < 25:
			goal_speed = 5
		elif 25 <= time < 30:
			goal_speed = -time + 30
		else:
			self.running = False
			
		return goal_speed	
		
		

	def on_shutdown(self):
		pass
		
	
if __name__ == '__main__':
	# Parse arguments
	parser = argparse.ArgumentParser(description='Empty ROS node')
	parser.add_argument('-d', '--debug', action='store_true', help='Print extra output to terminal.')
	args, unknown = parser.parse_known_args() # Only parse arguments defined above

	try:
		node = SpeedSignalPublisherNode(cmd_args = args)
	except rospy.ROSInterruptException:
		pass
	
	
