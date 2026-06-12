cmake_minimum_required(VERSION 3.5)
project(can_comm_pkg)

find_package(ament_cmake REQUIRED)

# Indica ament que instale el paquete Python
ament_python_install_package(${PROJECT_NAME})

ament_package()
