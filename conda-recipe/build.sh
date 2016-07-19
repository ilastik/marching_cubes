export CXXFLAGS=""
export CFLAGS=""
export LDFLAGS=""

# Depending on our platform, shared libraries end with either .so or .dylib
if [[ `uname` == 'Darwin' ]]; then
    DYLIB_EXT=dylib
else
    DYLIB_EXT=so
fi

CXXFLAGS="${CFLAGS} -std=c++11"

mkdir build
cd build
cmake ..\
    -DCMAKE_C_COMPILER=${PREFIX}/bin/gcc \
    -DCMAKE_CXX_COMPILER=${PREFIX}/bin/g++ \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS}" \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_PREFIX_PATH=${PREFIX} \
    -DPYTHON_EXECUTABLE=${PYTHON} \
    -DPYTHON_LIBRARY=${PREFIX}/lib/libpython2.7.${DYLIB_EXT} \
    -DPYTHON_INCLUDE_DIR=${PREFIX}/include/python2.7 \
##

make -j${CPU_COUNT}

# No install step yet.  Copy manually
#make install

cp ${SRC_DIR}/build/marching_cubes.so ${PREFIX}/lib/python2.7/site-packages/
