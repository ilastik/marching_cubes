mkdir build
cd build
cmake .. -G "%CMAKE_GENERATOR%" ^
    -DCMAKE_PREFIX_PATH="%LIBRARY_PREFIX%" ^
    -DCMAKE_INSTALL_PREFIX="%PREFIX%" ^
    -DPYTHON_EXECUTABLE="%PYTHON%"

if errorlevel 1 exit 1

cmake --build . --target ALL_BUILD --config %CONFIGURATION%
if errorlevel 1 exit 1

cmake --build . --target INSTALL --config %CONFIGURATION%
if errorlevel 1 exit 1
