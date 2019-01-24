cmake_minimum_required(VERSION 2.8.12)
project(marching_cubes)
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)


include(CheckCXXCompilerFlag)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    CHECK_CXX_COMPILER_FLAG("-std=c++11" HAS_CPP11_FLAG)
    if (HAS_CPP11_FLAG)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
    endif()
endif()

find_package(OpenMP)


find_package(Boost REQUIRED container)
include_directories(${Boost_INCLUDE_DIRS})


find_package(pybind11 REQUIRED)
include_directories(${pybind11_INCLUDE_DIRS})


if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()


# set(WINDOWS_EXPORT_ALL_SYMBOLS 1)
# set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS 1)


include_directories(src)

pybind11_add_module(marching_cubes
    src/python_wrapper.cpp
    src/marching_cubes.h
    src/marching_cubes.cpp
    src/laplacian_smoothing.h
    src/laplacian_smoothing.cpp)



#################################
# INSTALL THE PYTHON MODULE
#################################

if(NOT DEFINED PYTHON_MODULE_INSTALL_DIR OR PYTHON_MODULE_INSTALL_DIR MATCHES "^$")
  execute_process(COMMAND ${PYTHON_EXECUTABLE} -c
                    "from distutils.sysconfig import *; print(get_python_lib(1))"
                    OUTPUT_VARIABLE PYTHON_SITE_PACKAGES OUTPUT_STRIP_TRAILING_WHITESPACE)
  FILE(TO_CMAKE_PATH ${PYTHON_SITE_PACKAGES} PYTHON_MODULE_INSTALL_DIR)
endif()

SET(PYTHON_MODULE_INSTALL_DIR ${PYTHON_MODULE_INSTALL_DIR}
    CACHE PATH "where to install the marching cubres Python package" FORCE)

# this is the install path relative to CMAKE_INSTALL_PREFIX,
# use this in INSTALL() commands to get packaging right
FILE(RELATIVE_PATH PYTHON_MODULE_INSTALL_DIR ${CMAKE_INSTALL_PREFIX} ${PYTHON_MODULE_INSTALL_DIR})

install(TARGETS marching_cubes DESTINATION ${PYTHON_MODULE_INSTALL_DIR})