export CXXFLAGS=""
export CFLAGS=""
export LDFLAGS=""

PY_VER=$(python -c "import sys; print('{}.{}'.format(*sys.version_info[:2]))")
PY_ABIFLAGS=$(python -c "import sys; print('' if sys.version_info.major == 2 else sys.abiflags)")
PY_ABI=${PY_VER}${PY_ABIFLAGS}

# Depending on our platform, shared libraries end with either .so or .dylib
if [[ $(uname) == 'Darwin' ]]; then
    DYLIB_EXT=dylib
    CC=clang
    CXX=clang++
    CXXFLAGS="${CFLAGS} -std=c++11 -stdlib=libc++"
else
    DYLIB_EXT=so
    CC=gcc
    CXX=g++
    CXXFLAGS="${CFLAGS} -std=c++11"
    # enable compilation without CXX abi to stay compatible with gcc < 5 built packages
    if [[ ${DO_NOT_BUILD_WITH_CXX11_ABI} == '1' ]]; then
        CXXFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0 ${CXXFLAGS}"
    fi
fi

mkdir build
cd build
cmake ..\
    -DCMAKE_C_COMPILER=${CC} \
    -DCMAKE_CXX_COMPILER=${CXX} \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS}" \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_PREFIX_PATH=${PREFIX} \
    -DPYTHON_EXECUTABLE=${PYTHON} \
    -DPYTHON_LIBRARY=${PREFIX}/lib/libpython${PY_ABI}.${DYLIB_EXT} \
    -DPYTHON_INCLUDE_DIR=${PREFIX}/include/python${PY_ABI} \
    ${CXX_ABI_ARGS} \
##

make -j${CPU_COUNT}

make install

#cp ${SRC_DIR}/build/marching_cubes*.so ${PREFIX}/lib/python${PY_VER}/site-packages/
