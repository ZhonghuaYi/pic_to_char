cmake_minimum_required(VERSION 3.21)

set(CMAKE_CXX_STANDARD 17)
add_definitions(-std=c++17)
set(CMAKE_CXX_FLAGS "-std=c++17")

project(pic_to_char)

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    set(CMAKE_EXE_LINKER_FLAGS "-lcblas")
endif()

find_package(OpenCV REQUIRED)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
aux_source_directory(src SRC_LIST)
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${PROJECT_SOURCE_DIR}/include)

add_executable(pic_to_char ${SRC_LIST})
target_link_libraries(pic_to_char ${OpenCV_LIBS})

