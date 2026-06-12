#include "rclcpp/rclcpp.hpp"
#include "joint_state_listener.hpp"

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<JointStateListener>("joint_state_listener");
    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}
