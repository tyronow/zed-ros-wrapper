#!/usr/bin/env python

__author__ = "Tyrone Nowell"
__email__ = "tyrone.nowell@nibio.no"

import rospy
import tf
import tf2_ros

import geometry_msgs.msg

def main():
    rospy.init_node("zed_initialiser")

    listener = tf.TransformListener()
    br = tf2_ros.StaticTransformBroadcaster()
    trans, rot = None, None

    while not trans and not rot:
        # Look up the initial pose of the imu and zed
        try:
            now = rospy.Time.now()
            listener.waitForTransform('/odom', '/imu', now, rospy.Duration(2.0))
            (trans, rot) = listener.lookupTransform('/odom', '/imu', now)
        except (tf.Exception, tf.LookupException, tf.ConnectivityException):
            rospy.logwarn("Failed to find odom to imu transform")

        # Publish the initial pose for the ZED
        if(trans and rot):
            t = geometry_msgs.msg.TransformStamped()
            t.header.stamp = rospy.Time.now()
            t.header.frame_id = 'odom'
            t.child_frame_id = 'zed_init'

            # Apply -0.03m, 0.26m, 0.05m (X, Y, Z) translation
            t.transform.translation.x = trans[0] - 0.03
            t.transform.translation.y = trans[1] + 0.26
            t.transform.translation.z = trans[2] + 0.05

            # Apply 180 deg yaw and 45 deg pitch
            t.transform.rotation.x = rot[0] - 0.3826834
            t.transform.rotation.y = rot[1]
            t.transform.rotation.z = rot[2] + 0.9238795
            t.transform.rotation.w = rot[3]

            br.sendTransform(t)
            rospy.spin()

if __name__ == '__main__':
    main()
