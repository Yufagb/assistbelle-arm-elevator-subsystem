#ifndef JOINT_STATE_LISTENER_H
#define JOINT_STATE_LISTENER_H

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float32_multi_array.hpp>
#include <std_msgs/msg/string.hpp>
#include <string>

class JointStateListener : public rclcpp::Node
{
public:

    JointStateListener(
        const std::string & node_name,
        const std::string & pub_topic,
        const std::string & sub_topic,
        double frequency_hz);

    // Default: pub: /can_command, sub: /motors_state, hz: 20
    JointStateListener(const std::string & node_name);

private:
    void timer_callback();
    void motors_state_callback(const std_msgs::msg::Float32MultiArray::SharedPtr msg);

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr command_pub_;
    rclcpp::Subscription<std_msgs::msg::Float32MultiArray>::SharedPtr motors_state_sub_;
    rclcpp::TimerBase::SharedPtr timer_;

    std::string command_string_ = "A6";

};



#endif
