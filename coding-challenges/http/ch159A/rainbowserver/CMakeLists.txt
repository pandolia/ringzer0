project(rainbowserver)
cmake_minimum_required(VERSION 2.8)
aux_source_directory(. SRC_LIST)
add_executable(${PROJECT_NAME} ${SRC_LIST})

set(CMAKE_C_COMPILER "gcc")
set(CMAKE_C_FLAGS "-Wall -O2 -lcrypto")
