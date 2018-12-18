#! /usr/bin/env python
 
import rospy
from std_msgs.msg import Int16
from simple_pid import PID


class SteerPID(object):
	def __init__(self):
		self._sub_cte = rospy.Subscriber("/kitt/img_process/cte/", Int16 ,self.cte_callback)
	        self._pub_steer = rospy.Publisher("/kitt/steer_pid/value", Int16, queue_size = 1)
		self.pid = PID(1, 0.0, 0.0, setpoint=0)
		self.pid.sample_time = 0.01 
		self.pid.output_limits = (-100, 100)


	def cte_callback(self, data):
		output = self.pid(data.data)
		print('Cte:{}, Angle:{}'.format(data, output))
		self._pub_steer.publish(output)
		


def main():
    steer_pid = SteerPID()
    rospy.init_node('kitt_steer_pid', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main()
