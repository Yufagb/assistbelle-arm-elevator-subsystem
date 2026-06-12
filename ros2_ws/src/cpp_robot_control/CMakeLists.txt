cmake_minimum_required(VERSION 3.8)
project(cpp_robot_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# Eigen
find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIRS})

# add executeables
add_executable(joint_state_listener src/joint_state_listener/joint_state_listener.cpp
  src/joint_state_listener/main.cpp
  )

add_executable(joint_trajectory_controller src/joint_trajectory_controller/joint_trajectory_controller.cpp
  src/joint_trajectory_controller/main.cpp
  )

# Link libraries
target_include_directories(joint_state_listener PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src/joint_state_listener>
)

target_include_directories(joint_trajectory_controller PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src/joint_trajectory_controller>
)

target_link_libraries(joint_trajectory_controller
  ${OpenCV_LIBS}
  ${EIGEN_3_LIBS}
)

# Ament dependencies
ament_target_dependencies(joint_state_listener
  rclcpp
  std_msgs
)


ament_target_dependencies(joint_trajectory_controller
  rclcpp
  std_msgs
)


# Install
install(TARGETS
joint_state_listener
joint_trajectory_controller
DESTINATION lib/${PROJECT_NAME}
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
