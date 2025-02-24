from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()
    rviz_sim = FindPackageShare('rviz_sim')


    # Launching the rviz file with the model
    urdf_model = LaunchConfiguration('urdf_model', default='model_core.urdf.xacro')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    launch_jsb = LaunchConfiguration('launch_jsb', default='true')

    rviz_urdf_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([rviz_sim, 'launch', 'rviz_sim_launch.py'])
                ),
            launch_arguments={'use_sim_time': use_sim_time, 'urdf_model': urdf_model}.items()
            )

    # Launching an empty gazebo gui and server
    world = LaunchConfiguration('world', default='empty.sdf')

    ign_gz_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([rviz_sim, 'launch', 'gazebo_launch.py'])
                ),
            launch_arguments={'world': world}.items()
            )

    # Launching the controller nodes
    controller_manager=IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([rviz_sim, 'launch', 'robot_controller.py'])),
            launch_arguments={'launch_jsb': launch_jsb}.items()
            )

    # Launching ros_gz_sim to get information for robot_description topic
    spawn_robot = Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', '/robot_description'],
            output='screen')
            
    ld.add_action(rviz_urdf_launch)
    ld.add_action(ign_gz_launch)
    ld.add_action(spawn_robot)
    ld.add_action(controller_manager)
    return ld
