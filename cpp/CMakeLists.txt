cmake_minimum_required(VERSION 3.21)
project(pic_to_char)

set(CMAKE_CXX_STANDARD 14)

find_package(OpenCV REQUIRED)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
aux_source_directory(src SRC_LIST)
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${PROJECT_SOURCE_DIR}/include)

add_executable(pic_to_char ${SRC_LIST})
target_link_libraries(pic_to_char ${OpenCV_LIBS})

