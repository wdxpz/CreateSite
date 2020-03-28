
# Requirement

## [Wand](docs.wand-py.org/en/0.5.9)
a ctypes-based simple [ImageMagick](www.imagemagick.org) binding for Python
```
sudo apt-get install libmagickwand-dev
pip install Wand
```

#Launch
## Start Robot
1. in turtulebot master
```
$ roscore
```
2. in turtulebot 
```
$ roslaunch turtlebot3_bringup turtlebot3_robot.launch
```
3. in turtlebot master, do the slam or launch navigation using exitsted map
```
$ export TURTLEBOT3_MODEL=${TB3_MODEL}
$ roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping
$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

# or launch naviagation
$ roslaunch turtlebot3_navigation turtlebot3_navigation.launch open_rviz:=false initial_pose_x:=0 initial_pose_y:=0 initial_pose_a:=0 update_min_d:=0.1 update_min_a:=0.2 map_file:=/home/waffle/map/map.yaml
```

4. export map and create site in remote db
```
python3 createsite.py -s <sitename> -d <description>
```