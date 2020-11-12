#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from pds_client.srv import GetPallet, GetPalletResponse
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse

PDS_NO_ERRORS = 0
PDS_TYPE_UNSUPPORTED = -1001
PDS_NOT_ENOUGH_POCKET_SIDES = -1036

class PdsClient:


    def __init__(self):


        rospy.init_node('gazebo_pds_client', anonymous=True)


        rospy.wait_for_service('pallet_detection/trigger')
        self.start_detection = rospy.ServiceProxy('pallet_detection/trigger', Trigger)

        self.pds_pallet_detector_server = rospy.Service('pds/client/GetPallet', GetPallet, self.callback_pds_pallet_detector_server)
        
        self.pds_pallet_pose_publisher = rospy.Publisher('pds/client/pallet_pose', PoseStamped  , queue_size=1)

        self.gazebo_pallet_tracking = rospy.Subscriber('pallet_detection/pose_triggered', PoseStamped, self.callback_gazebo_pallet_tracking)

        rospy.loginfo("Node ready!")


    def callback_pds_pallet_detector_server (self, req):
        
        # Simulate the process time
        rospy.sleep(1.0)

        # Build server response
        res_pds = GetPalletResponse()
        

        res_detection = TriggerResponse 
        res_detection = self.start_detection()        
        
        if res_detection.success == True:
            res_pds.status = PDS_NO_ERRORS
        else:
            res_pds.status = PDS_NOT_ENOUGH_POCKET_SIDES

        return res_pds

    def callback_gazebo_pallet_tracking(self, pallet_pose):

        self.pds_pallet_pose_publisher.publish(pallet_pose)

    def run(self):

            rospy.spin()


if __name__ == '__main__':

    pds_client = PdsClient()

    try:
        pds_client.run()

    except rospy.ROSInterruptException:
        pass
