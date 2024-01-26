import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node, SetParameter
import xacro
import os


def generate_launch_description():
    ld = LaunchDescription()

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'seaborgium_description'

    file_subpath = 'urdf/seaborgium.xacro.urdf'

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name), file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Include the Gazebo launch file
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('coursework2'), '/launch', '/sim_bringup.launch.py']),
        launch_arguments={}.items(),
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}]
    )

    # Run the spawner node from the gazebo_ros package.
    node_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', '/robot_description', '-z', '0.5'],
        output='screen'
    )

    # Define a ROS 2 node to bridge communication between ROS 2 and Ignition Gazebo
    node_ros_gz_bridge = Node(
    package = 'ros_gz_bridge',
    executable = 'parameter_bridge',
        # Arguments specifying the topic names and message types for bridging
    arguments = [
        '/model/seaborgium/cmd_vel'                 + '@geometry_msgs/msg/Twist'    + '@' + 'ignition.msgs.Twist',
        '/model/seaborgium/odometry'                + '@nav_msgs/msg/Odometry'      + '[' + 'ignition.msgs.Odometry',
        '/model/seaborgium/scan'                    + '@sensor_msgs/msg/LaserScan'  + '[' + 'ignition.msgs.LaserScan',
        '/model/seaborgium/tf'                      + '@tf2_msgs/msg/TFMessage'     + '[' + 'ignition.msgs.Pose_V',
        '/model/seaborgium/imu'                     + '@sensor_msgs/msg/Imu'        + '[' + 'ignition.msgs.IMU',
        '/model/seaborgium/depth'                   + '@sensor_msgs/msg/Image'      + '[' + 'ignition.msgs.Image',
        '/world/empty/model/seaborgium/joint_state' + '@sensor_msgs/msg/JointState' + '[' + 'ignition.msgs.Model',
    ],
        #Ensuring reliable communication
    parameters = [{'qos_overrides./seaborgium.subscriber.reliability': 'reliable'}],
        # Remappings to change topic names for communication with Gazebo
    remappings = [
        ('/model/seaborgium/cmd_vel'                , '/seaborgium/cmd_vel'),
        ('/model/seaborgium/odometry'               , '/odom_raw'),
        ('/model/seaborgium/scan'                   , '/scan'),
        ('/model/seaborgium/imu'                    , '/imu_raw'),
        ('/model/seaborgium/tf'                     , '/tf'),
        ('/model/seaborgium/depth'                  , '/depth'),
        ('/world/empty/model/seaborgium/joint_state', 'joint_states'),
    ],
    output='screen'
    )

    #locating our params file for input
    teleop_params = os.path.join(get_package_share_directory('seaborgium_description'),'config','params.yaml')

    #Create a twist mux node for multiple inputs with priority
    twist_mux = Node(
        package='twist_mux',
        executable='twist_mux',
        name='twist_mux',
        output='screen',
        parameters=[{teleop_params}],
        remappings=[
            ('cmd_vel_out', '/seaborgium/cmd_vel'),
        ],
    )
    
    # Teleop node
    node_teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist',
        output='screen',
        remappings=[('/cmd_vel', '/teleop_cmd_vel')],
    )

    # Add actions to LaunchDescription
    ld.add_action(SetParameter(name='use_sim_time', value=True))
    ld.add_action(twist_mux)
    ld.add_action(robot_state_publisher)
    ld.add_action(node_spawn_entity)
    ld.add_action(node_ros_gz_bridge)
    ld.add_action(node_teleop)
    ld.add_action(launch_gazebo)
    return ld
