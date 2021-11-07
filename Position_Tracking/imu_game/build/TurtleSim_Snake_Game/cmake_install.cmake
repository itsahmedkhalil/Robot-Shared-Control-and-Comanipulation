# Install script for directory: /home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_game/src/TurtleSim_Snake_Game

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_game/install")
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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_game/build/TurtleSim_Snake_Game/catkin_generated/installspace/turtle_snake_game.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/turtle_snake_game/cmake" TYPE FILE FILES
    "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_game/build/TurtleSim_Snake_Game/catkin_generated/installspace/turtle_snake_gameConfig.cmake"
    "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_game/build/TurtleSim_Snake_Game/catkin_generated/installspace/turtle_snake_gameConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/turtle_snake_game" TYPE FILE FILES "/home/ahmed/Desktop/research/Robot-Shared-Control-and-Comanipulation/Position_Tracking/imu_game/src/TurtleSim_Snake_Game/package.xml")
endif()

