cmake_minimum_required(VERSION 2.8.12)
project(marching_cubes)
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)










include(CheckCXXCompilerFlag)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


# FIXME c++14 checks are broken!?!
if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    CHECK_CXX_COMPILER_FLAG("-std=c++14" HAS_CPP14_FLAG)
    if (HAS_CPP14_FLAG)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
    endif()
endif()

# WITH_LP_MP needs special treatment since
# it requires C++ 14 and used OpenMP
if(WITH_LP_MP)
    find_package(OpenMP)
    if (OPENMP_FOUND)
        set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
        set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    endif()

endif()





find_package(OpenMP)

find_package(xtensor REQUIRED)
include_directories(${xtensor_INCLUDE_DIRS})

find_package(xtensor-python REQUIRED)
include_directories(${xtensor-python_INCLUDE_DIRS})

find_package(pybind11 REQUIRED)
include_directories(${pybind11_INCLUDE_DIRS})

find_package(NUMPY REQUIRED)
include_directories(${PYTHON_NUMPY_INCLUDE_DIR})



if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()


set(WINDOWS_EXPORT_ALL_SYMBOLS 1)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS 1)


include_directories(src)

pybind11_add_module(marching_cubes 
    src/python_wrapper.cpp
    src/marching_cubes.h 
    src/marching_cubes.cpp
    src/laplacian_smoothing.h 
    src/laplacian_smoothing.cpp)
