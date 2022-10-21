#!/usr/bin/env python3

import string
import rosbag

bagdir = "../bags/"
# Set name of the outbag
with rosbag.Bag(bagdir + 'Output_Locobot_DAN407.bag', 'w') as outbag:
    # Read a bagfile and iterate over all the messages
    # for topic, msg, t in rosbag.Bag('2022-09-28-16-06-12.bag').read_messages():
    for topic, msg, t in rosbag.Bag(bagdir + '2022-09-29-20-00-53.bag').read_messages():
    # for topic, msg, t in rosbag.Bag('Output_Locobot_DAN407.bag').read_messages():
        # Select the messages in the /tf_static topic which are tf2/TFMessages
        if topic == "/tf_static":
            if msg.transforms:
                # Remove locobot/ from the frame_id of the header and child_frame_id
                for transform in msg.transforms:
                    transform.header.frame_id = transform.header.frame_id.replace('locobot/','')
                    transform.child_frame_id = transform.child_frame_id.replace('locobot/','')
                #Write to new bagfile
            outbag.write(topic, msg, t)
        elif topic == "/locobot/tf" or topic == "/tf":
            if msg.transforms:
                for transform in msg.transforms:
                    transform.header.frame_id = transform.header.frame_id.replace('locobot/','')
                    transform.child_frame_id = transform.child_frame_id.replace('locobot/','')
            outbag.write('/tf', msg, msg.header.stamp if msg._has_header else t)
            # outbag.write('/tf', msg, t)
        elif topic == "/locobot/scan":
            # Remove locobot/ from the frame_id
            msg.header.frame_id = msg.header.frame_id.replace('locobot/','')
            # msg.header.frame_id = "lidar_tower_link"
            outbag.write('/scan', msg, msg.header.stamp if msg._has_header else t)
            # outbag.write('/scan', msg, t)
        elif topic == "/locobot/odom":
            outbag.write('/odom', msg, msg.header.stamp if msg._has_header else t)
            # outbag.write('/odom', msg, t)
        # else:
        #     topic = topic.replace('locobot/','')
        #     # outbag.write(topic, msg, msg.header.stamp if msg._has_header else t)
        #     outbag.write(topic, msg, msg.header.stamp if msg._has_header else t)
