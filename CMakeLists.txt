cmake_minimum_required(VERSION 2.8.12)
project(marching_cubes)

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()


set(WINDOWS_EXPORT_ALL_SYMBOLS 1)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS 1)

add_subdirectory(pybind11)
include_directories(src)
pybind11_add_module(marching_cubes src/python_wrapper.cpp src/marching_cubes.h src/marching_cubes.cpp src/laplacian_smoothing.h src/laplacian_smoothing.cpp)
