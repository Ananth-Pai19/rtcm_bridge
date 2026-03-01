Run the publisher on the base station laptop
python3 rtcm_publisher.py

Run the ublox_gps node on the Jetson Orin Nano
ros2 run ublox_gps ublox_gps_node --ros-args --params-file zed_f9p_rover.yaml 
(Give the correct file path)

The correct GNSS will come on the topic /fix

rtcm_subscriber.py is not used currently
