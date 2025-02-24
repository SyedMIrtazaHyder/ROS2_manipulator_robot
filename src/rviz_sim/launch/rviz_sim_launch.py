from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, Command

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()

    rviz_sim = FindPackageShare('rviz_sim')
    urdf_model = DeclareLaunchArgument(name='urdf_model', default_value='model_core.urdf.xacro',
            description="Name of the urdf to be displayed by rviz")
    use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='false',
            description="For syncing Gazebo Simulator with Rviz")

    # Adding default config params to the rviz world
    rviz2_default_config_path = 'basic_config.rviz'
    rviz2_config = DeclareLaunchArgument(name='rviz2_config', default_value=rviz2_default_config_path, description="Sets rviz environment configurations")

    rviz2 = Node(
            executable='rviz2',
            package='rviz2',
            name="rviz_node",
            arguments=['-d', PathJoinSubstitution([rviz_sim, 'config', LaunchConfiguration('rviz2_config')])]
            )

    robot_state_publisher = Node(
            executable='robot_state_publisher',
            package='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro', ' ', PathJoinSubstitution([rviz_sim, 'urdf', LaunchConfiguration('urdf_model')])]), 'use_sim_time': LaunchConfiguration('use_sim_time'),
                'debug': True
                }]
            )

    ld.add_action(rviz2_config)
    ld.add_action(use_sim_time)
    ld.add_action(urdf_model)
    ld.add_action(rviz2)
    ld.add_action(robot_state_publisher)

    # Goal 2: Launching rviz world with arguments a) rviz.config b) urdf model
    return ld
