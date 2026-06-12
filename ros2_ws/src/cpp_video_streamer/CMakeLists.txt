cmake_minimum_required(VERSION 3.8)
project(cpp_video_streamer)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)



# gst video streamer deps
find_package(PkgConfig REQUIRED)
pkg_check_modules(GSTREAMER REQUIRED gstreamer-1.0)
pkg_check_modules(GSTREAMER_RTSP_SERVER REQUIRED gstreamer-rtsp-server-1.0)
pkg_check_modules(GST REQUIRED gstreamer-1.0>=1.18 gstreamer-app-1.0)
include_directories(
  ${OpenCV_INCLUDE_DIRS}
  ${GSTREAMER_INCLUDE_DIRS}
  ${GSTREAMER_RTSP_SERVER_INCLUDE_DIRS}
)

# OpenCV
find_package(OpenCV REQUIRED)

# Adding executeables
add_executable(gst_video_streamer src/gst_video_streamer.cpp)
add_executable(gst_opencv_test src/gst_opencv_test.cpp)

target_include_directories(gst_video_streamer PRIVATE ${GSTREAMER_INCLUDE_DIRS})

target_link_libraries(gst_video_streamer
  ${GSTREAMER_LIBRARIES}
  ${GSTREAMER_RTSP_SERVER_LIBRARIES}
)

target_link_libraries(gst_opencv_test
  ${OpenCV_LIBS}
  ${GSTREAMER_LIBRARIES}
  ${GST_LIBRARIES}
)

# Ament dependencies
ament_target_dependencies(gst_video_streamer rclcpp)
ament_target_dependencies(gst_opencv_test rclcpp)

install(TARGETS
gst_video_streamer
gst_opencv_test
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
