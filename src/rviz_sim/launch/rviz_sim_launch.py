from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()

    # Adding default config params to the rviz world
    rviz_sim = FindPackageShare('rviz_sim')
    rviz2_default_config_path = 'basic_config.rviz'
    rviz2_config = DeclareLaunchArgument(name='rviz2_config', default_value=rviz2_default_config_path, description="Sets rviz environment configurations")

    # Goal 1: Launching Blank rviz world using the launch file
    rviz2 = Node(
            executable='rviz2',
            package='rviz2',
            arguments=['-d', PathJoinSubstitution([rviz_sim, 'config', LaunchConfiguration('rviz2_config')])]
            )

    ld.add_action(rviz2_config)
    ld.add_action(rviz2)

    # Goal 2: Launching rviz world with arguments a) rviz.config b) urdf model
    return ld
