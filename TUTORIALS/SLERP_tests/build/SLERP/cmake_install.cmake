# Install script for directory: /home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/install")
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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/SLERP/msg" TYPE FILE FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/msg/Num.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/SLERP/cmake" TYPE FILE FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/build/SLERP/catkin_generated/installspace/SLERP-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/devel/include/SLERP")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/devel/share/roseus/ros/SLERP")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/devel/share/common-lisp/ros/SLERP")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/devel/share/gennodejs/ros/SLERP")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/devel/lib/python3/dist-packages/SLERP")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/devel/lib/python3/dist-packages/SLERP")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/build/SLERP/catkin_generated/installspace/SLERP.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/SLERP/cmake" TYPE FILE FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/build/SLERP/catkin_generated/installspace/SLERP-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/SLERP/cmake" TYPE FILE FILES
    "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/build/SLERP/catkin_generated/installspace/SLERPConfig.cmake"
    "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/build/SLERP/catkin_generated/installspace/SLERPConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/SLERP" TYPE FILE FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/src/SLERP/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/SLERP" TYPE PROGRAM FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/build/SLERP/catkin_generated/installspace/slerper.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/SLERP" TYPE PROGRAM FILES "/home/mohamed/Robot-Shared-Control-and-Comanipulation/TUTORIALS/SLERP_tests/build/SLERP/catkin_generated/installspace/listen.py")
endif()

