cmake_minimum_required(VERSION 2.8.12)
project(XxhashTest C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

add_executable(xxhash_test "main.c")
target_link_libraries(xxhash_test ${CONAN_LIBS})
