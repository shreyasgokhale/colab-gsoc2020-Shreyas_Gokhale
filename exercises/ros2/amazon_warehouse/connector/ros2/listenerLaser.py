import threading
from math import pi as PI

import rclpy
from jderobotTypes import LaserData
from sensor_msgs.msg import LaserScan


def laserScan2LaserData(scan):
    '''
    Translates from ROS LaserScan to JderobotTypes LaserData. 

    @param scan: ROS LaserScan to translate

    @type scan: LaserScan

    @return a LaserData translated from scan

    '''
    laser = LaserData()
    laser.values = scan.ranges
    ''' 
          ROS Angle Map      JdeRobot Angle Map
                0                  PI/2
                |                   |
                |                   |
       PI/2 --------- -PI/2  PI --------- 0
                |                   |
                |                   |
    '''
    laser.minAngle = scan.angle_min + PI / 2
    laser.maxAngle = scan.angle_max + PI / 2
    laser.maxRange = scan.range_max
    laser.minRange = scan.range_min
    laser.timeStamp = scan.header.stamp.secs + (scan.header.stamp.nsecs * 1e-9)
    return laser


class ListenerLaser:
    """
        ROS Laser Subscriber. Laser Client to Receive Laser Scans from ROS nodes.
    """

    def __init__(self, topic):
        """
        ListenerLaser Constructor.

        @param topic: ROS topic to subscribe

        @type topic: String

        """
        self.ros_node = rclpy.create_node('laser_listener')
        self.topic = topic
        self.data = LaserData()
        self.sub = None
        self.lock = threading.Lock()
        self.start()

    def __callback(self, scan):
        """
        Callback function to receive and save Laser Scans.

        @param scan: ROS LaserScan received

        @type scan: LaserScan

        """
        laser = laserScan2LaserData(scan)

        self.lock.acquire()
        self.data = laser
        self.lock.release()

    def stop(self):
        """
        Stops (Unregisters) the client.

        """
        self.sub.unregister()

    def start(self):
        """
        Starts (Subscribes) the client.

        """
        # self.sub = self.ros_node.create_subscription(LaserScan, self.topic,  self.__callback)
        self.sub = self.ros_node.create_subscription(LaserScan, self.topic,  self.__callback, 10)

    def getLaserData(self):
        """
        Returns last LaserData.

        @return last JdeRobotTypes LaserData saved

        """
        self.lock.acquire()
        laser = self.data
        self.lock.release()

        return laser
