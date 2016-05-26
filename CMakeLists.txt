cmake_minimum_required(VERSION 3.5.0)

project(mesmeproj)

# C++11 standard.
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find includes in corresponding build directories.
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# Run moc automatically.
set(CMAKE_AUTOMOC ON)

# Set the prefix path.
set(CMAKE_PREFIX_PATH "" CACHE PATH "CMake prefix path")

# Set the gui type.
if(WIN32)
    set(GUI_TYPE WIN32)
elseif(APPLE)
    set(GUI_TYPE MACOSX_BUNDLE)
endif()

# Find Qt.
find_package(Qt5Core REQUIRED)
find_package(Qt5Qml REQUIRED)
find_package(Qt5Quick REQUIRED)

# Add the qrc resource.
QT5_ADD_RESOURCES(MESME_QRC src/mesme.qrc)

# Add the main executable.
add_executable(mesme ${GUI_TYPE}
        src/mesme.cpp
        src/ui/mmMainWindow.cpp
        ${MESME_QRC}
)
target_link_libraries(mesme
        Qt5::Core
        Qt5::Qml
        Qt5::Quick
)
