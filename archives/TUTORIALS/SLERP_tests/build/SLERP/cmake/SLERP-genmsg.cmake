# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "SLERP: 1 messages, 0 services")

set(MSG_I_FLAGS "-ISLERP:/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(SLERP_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg" NAME_WE)
add_custom_target(_SLERP_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "SLERP" "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg" "geometry_msgs/Quaternion"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(SLERP
  "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/SLERP
)

### Generating Services

### Generating Module File
_generate_module_cpp(SLERP
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/SLERP
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(SLERP_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(SLERP_generate_messages SLERP_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg" NAME_WE)
add_dependencies(SLERP_generate_messages_cpp _SLERP_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(SLERP_gencpp)
add_dependencies(SLERP_gencpp SLERP_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS SLERP_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(SLERP
  "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/SLERP
)

### Generating Services

### Generating Module File
_generate_module_eus(SLERP
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/SLERP
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(SLERP_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(SLERP_generate_messages SLERP_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg" NAME_WE)
add_dependencies(SLERP_generate_messages_eus _SLERP_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(SLERP_geneus)
add_dependencies(SLERP_geneus SLERP_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS SLERP_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(SLERP
  "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/SLERP
)

### Generating Services

### Generating Module File
_generate_module_lisp(SLERP
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/SLERP
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(SLERP_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(SLERP_generate_messages SLERP_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg" NAME_WE)
add_dependencies(SLERP_generate_messages_lisp _SLERP_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(SLERP_genlisp)
add_dependencies(SLERP_genlisp SLERP_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS SLERP_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(SLERP
  "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/SLERP
)

### Generating Services

### Generating Module File
_generate_module_nodejs(SLERP
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/SLERP
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(SLERP_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(SLERP_generate_messages SLERP_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg" NAME_WE)
add_dependencies(SLERP_generate_messages_nodejs _SLERP_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(SLERP_gennodejs)
add_dependencies(SLERP_gennodejs SLERP_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS SLERP_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(SLERP
  "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/SLERP
)

### Generating Services

### Generating Module File
_generate_module_py(SLERP
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/SLERP
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(SLERP_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(SLERP_generate_messages SLERP_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg" NAME_WE)
add_dependencies(SLERP_generate_messages_py _SLERP_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(SLERP_genpy)
add_dependencies(SLERP_genpy SLERP_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS SLERP_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/SLERP)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/SLERP
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(SLERP_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(SLERP_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/SLERP)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/SLERP
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(SLERP_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(SLERP_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/SLERP)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/SLERP
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(SLERP_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(SLERP_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/SLERP)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/SLERP
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(SLERP_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(SLERP_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/SLERP)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/SLERP\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/SLERP
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(SLERP_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(SLERP_generate_messages_py geometry_msgs_generate_messages_py)
endif()
