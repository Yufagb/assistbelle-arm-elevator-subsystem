#include "rclcpp/rclcpp.hpp"
#include "joint_trajectory_controller.hpp"

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<JointTrajectoryController>("joint_trajectory_controller");
    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}
