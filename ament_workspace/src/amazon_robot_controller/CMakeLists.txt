cmake_minimum_required(VERSION 3.5)
project(amazon_robot_controller)

find_package(ament_cmake REQUIRED)
find_package(nav2_common REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(amazon_robot_bt REQUIRED)
find_package(nav2_behavior_tree REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(behaviortree_cpp_v3 REQUIRED)
find_package(std_srvs REQUIRED)
find_package(nav2_util REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(amazon_robot_msg REQUIRED)

nav2_package()

include_directories(
  include
)

set(executable_name robot_controller)

add_executable(${executable_name}
  src/main.cpp
)

set(library_name ${executable_name}_core)


add_library(${library_name} SHARED
  src/robot_controller.cpp
  src/ros_topic_logger.cpp
)

set(dependencies
  rclcpp
  rclcpp_action
  rclcpp_lifecycle
  std_msgs
  geometry_msgs
  amazon_robot_bt
  nav2_behavior_tree
  nav_msgs
  nav2_msgs
  behaviortree_cpp_v3
  std_srvs
  nav2_util
  tf2_ros
  amazon_robot_msg
)

add_library(amazon_robot_all_goals_achieved_condition_bt_node SHARED plugins/condition/all_goals_achieved_condition.cpp)
list(APPEND plugin_libs amazon_robot_all_goals_achieved_condition_bt_node)

add_library(amazon_robot_get_next_goal_action_bt_node SHARED plugins/action/get_next_goal_action.cpp )
list(APPEND plugin_libs amazon_robot_get_next_goal_action_bt_node)

add_library(amazon_robot_load_pallet_action_bt_node SHARED plugins/action/LoadPallet.cpp)
list(APPEND plugin_libs amazon_robot_load_pallet_action_bt_node)

foreach(bt_plugin ${plugin_libs})
  ament_target_dependencies(${bt_plugin} ${dependencies})
  target_compile_definitions(${bt_plugin} PRIVATE BT_PLUGIN_EXPORT)
endforeach()


ament_target_dependencies(${executable_name}
  ${dependencies}
)
target_link_libraries(${executable_name} ${library_name})

ament_target_dependencies(${library_name}
  ${dependencies}
)


install(TARGETS ${library_name}
                ${plugin_libs}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(TARGETS ${executable_name}
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/
)

install(DIRECTORY behavior_trees DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_include_directories(include)

ament_export_libraries(
  ${plugin_libs}
)

ament_package()
