from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()
    rviz_sim = FindPackageShare('rviz_sim')

    world = DeclareLaunchArgument(name='world', default_value='empty.sdf',
            description="World to load in Gazebo")

    set_env_vars = AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([rviz_sim, 'urdf'])
            )

    gz_server_cmd = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('ros_gz_sim'),
                    'launch',
                    'gz_sim.launch.py'])
                ),
            launch_arguments={'gz_args': PathJoinSubstitution([rviz_sim, 'worlds', LaunchConfiguration('world')])}.items()
            )

    ld.add_action(world)
    ld.add_action(set_env_vars)
    ld.add_action(gz_server_cmd)

    return ld
