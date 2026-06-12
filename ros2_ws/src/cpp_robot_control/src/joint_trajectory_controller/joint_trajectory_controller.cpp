
#include "joint_trajectory_controller.hpp"

JointTrajectoryController::JointTrajectoryController(
        const std::string & node_name,
        const std::string & pub_topic,
        const std::string & sub_topic,
        double frequency_hz)
    : Node(node_name)
{
    // Control variables
    this->motor_state = new float[4];
    this->desired_state = new float[4];
    
    // Publisher
    command_pub_ = this->create_publisher<std_msgs::msg::String>(
        pub_topic, 10);

    // Subscriber
    motors_state_sub_ = this->create_subscription<std_msgs::msg::Float32MultiArray>(
        sub_topic, 10,
        std::bind(&JointTrajectoryController::motors_state_callback, this, std::placeholders::_1));

    // Timer
    auto period = std::chrono::duration<double>(1.0 / frequency_hz);
    timer_ = this->create_wall_timer(
        period,
        std::bind(&JointTrajectoryController::timer_callback, this));

    RCLCPP_INFO(this->get_logger(), "JointTrajectoryController started:");
    RCLCPP_INFO(this->get_logger(), " Publishing \"%s\" on: %s", 
                state_request_string_.c_str(), pub_topic.c_str());
    RCLCPP_INFO(this->get_logger(), " Subscribing to: %s", sub_topic.c_str());
    RCLCPP_INFO(this->get_logger(), " Frequency: %.2f Hz", frequency_hz);
    
}

// Delegated constructor
JointTrajectoryController::JointTrajectoryController(const std::string & node_name)
    : JointTrajectoryController(
        node_name,
        "/can_command",
        "/motors_state",
        100.0F           
      ){}



void JointTrajectoryController::timer_callback()
{
    // Run second order filter

    
    // State request
    std_msgs::msg::String cmd_msg;
    cmd_msg.data = state_request_string_;
    command_pub_->publish(cmd_msg);
    

}

void JointTrajectoryController::motors_state_callback(
    const std_msgs::msg::Float32MultiArray::SharedPtr msg)
{
    if (msg->data.size() < 10) {
        RCLCPP_WARN(this->get_logger(), "Motor state message too small! Expected 10 values.");
        return;
    }

    float q1 = msg->data[0], q2 = msg->data[1];
    float q3 = msg->data[2], q4 = msg->data[3];
    float dq1 = msg->data[5], dq2 = msg->data[6];
    float dq3 = msg->data[7], dq4 = msg->data[8];

    RCLCPP_INFO(this->get_logger(),
        "q=[%.2f %.2f %.2f %.2f], dq=[%.2f %.2f %.2f %.2f]",
        q1, q2, q3, q4, dq1, dq2, dq3, dq4);
}