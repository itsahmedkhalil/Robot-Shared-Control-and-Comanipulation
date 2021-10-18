# Install script for directory: /home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/src/imu_communication

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/imu_communication/msg" TYPE FILE FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/src/imu_communication/msg/Num.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/imu_communication/cmake" TYPE FILE FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/build/imu_communication/catkin_generated/installspace/imu_communication-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/devel/include/imu_communication")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/devel/share/roseus/ros/imu_communication")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/devel/share/common-lisp/ros/imu_communication")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/devel/share/gennodejs/ros/imu_communication")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/devel/lib/python3/dist-packages/imu_communication")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/devel/lib/python3/dist-packages/imu_communication")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/build/imu_communication/catkin_generated/installspace/imu_communication.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/imu_communication/cmake" TYPE FILE FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/build/imu_communication/catkin_generated/installspace/imu_communication-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/imu_communication/cmake" TYPE FILE FILES
    "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/build/imu_communication/catkin_generated/installspace/imu_communicationConfig.cmake"
    "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/build/imu_communication/catkin_generated/installspace/imu_communicationConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/imu_communication" TYPE FILE FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/src/imu_communication/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/imu_communication" TYPE PROGRAM FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/build/imu_communication/catkin_generated/installspace/pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/imu_communication" TYPE PROGRAM FILES "/home/mohamed/Desktop/Fall_Research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_ws/build/imu_communication/catkin_generated/installspace/sub.py")
endif()

