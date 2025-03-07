from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import PythonExpression, LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    launch_jsb = DeclareLaunchArgument(name='launch_jsb', default_value='false',
            description="Variable to launch the joint_state_broadcaster controller")
    controller_config = DeclareLaunchArgument(name='controller', default_value='wing_position_controller',
            description="Varibale to tell which control file to launch, either controlling only the slider joints or both the slider and revolute joints")

    # Launching ros2_controls node
    wing_controller = Node(
            package="controller_manager",
            executable="spawner",
            name="wings_controller",
            arguments=[LaunchConfiguration('controller')]
            )

    # Launching joint state broadcaster
    jsb = Node(
            package="controller_manager",
            executable="spawner",
            name="joint_state_broadcaster",
            arguments=["joint_state_broadcaster"],
            condition=IfCondition(LaunchConfiguration('launch_jsb'))
            )

    ld.add_action(controller_config)
    ld.add_action(wing_controller)
    ld.add_action(launch_jsb)
    ld.add_action(jsb)
    return ld
