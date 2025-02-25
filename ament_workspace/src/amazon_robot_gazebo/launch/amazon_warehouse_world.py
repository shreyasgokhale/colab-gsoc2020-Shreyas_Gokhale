#!/usr/bin/env python3
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')


    # world_file_name = 'amazon_warehouse.world'
    # world = os.path.join(get_package_share_directory('amazon_robot_gazebo'), 'worlds', world_file_name)
    # launch_file_dir = os.path.join(get_package_share_directory('amazon_robot_gazebo'), 'launch')

    world_file_name = 'empty_worlds/amazon_robot.model'
    world = os.path.join(get_package_share_directory('amazon_robot_gazebo'), 'worlds', world_file_name)
    launch_file_dir = os.path.join(get_package_share_directory('amazon_robot_gazebo'), 'launch')

    # sdf_file_name = 'amazon_robot2/model.sdf'
    # sdf = os.path.join(
    #     get_package_share_directory('amazon_robot_gazebo'),
    #     'models',
    #     sdf_file_name)

    # urdf_file_name = 'amazon_warehouse_robot.urdf.xacro'
    # urdf = os.path.join(
    #     get_package_share_directory('amazon_robot_description'),
    #     'urdf',
    #     urdf_file_name)

    # xml = open(sdf, 'r').read()

    # xml = xml.replace('"', '\\"')

    # swpan_args = '{name: \"amazon_robot\", xml: \"'  +  xml + '\" }'


    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so'],
            output='screen'),
    
        # ExecuteProcess(
        #     cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
        #     output='screen'),


            
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        
        # ExecuteProcess(
        #     cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', swpan_args],
        #     output='screen'),
    ])