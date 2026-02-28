cmake_minimum_required(VERSION 3.12)
project(MyPackage CXX)

# --- General Setup ---
# Specify C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Option for custom debug optimization level (O0, O1, O2, etc.)
set(DEBUG_OPT_LEVEL "O0" CACHE STRING "Optimization level for Debug build (e.g., O0, O1, O2)")

# Apply custom debug optimization level
if(CMAKE_BUILD_TYPE MATCHES "Debug")
    message(STATUS "Debug Build: Custom optimization level set to -${DEBUG_OPT_LEVEL}")

    # GCC / Clang
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        # Replace the default -O0 with our custom -O*
        # We also need to consider -O3 now.
        if(CMAKE_CXX_FLAGS_DEBUG MATCHES "-O[0-9]")
            string(REGEX REPLACE "-O[0-9]" "-${DEBUG_OPT_LEVEL}" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
        else()
            set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -${DEBUG_OPT_LEVEL}")
        endif()
    # MSVC
    elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
        # MSVC uses /Od (O0), /O1, /O2. We do a rough mapping.
        if(DEBUG_OPT_LEVEL STREQUAL "O0")
            set(MSVC_OPT "/Od")
        elseif(DEBUG_OPT_LEVEL STREQUAL "O1")
            set(MSVC_OPT "/O1")
        else()
            set(MSVC_OPT "/O2")
        endif()
        string(REGEX REPLACE "/Od" "${MSVC_OPT}" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
        string(REGEX REPLACE "/O1" "${MSVC_OPT}" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
        string(REGEX REPLACE "/O2" "${MSVC_OPT}" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")

        if(NOT CMAKE_CXX_FLAGS_DEBUG MATCHES "/O[d12]")
             set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} ${MSVC_OPT}")
        endif()
    endif()
endif()

message(STATUS "CMAKE_CXX_FLAGS_DEBUG: ${CMAKE_CXX_FLAGS_DEBUG}")

# --- Automatic Source File Discovery ---
# Recursively find all source and header files
file(GLOB_RECURSE LIB_HDRS "include/*.h")
file(GLOB_RECURSE LIB_SRCS "src/*.cpp")

# Exclude main.cpp from the library sources, because it's meant for the executable
list(FILTER LIB_SRCS EXCLUDE REGEX "src/main.cpp$")

# --- Library Target ---
# We define an object library or static library here.
# We'll use a static library for simplicity.
add_library(MyPackageLib STATIC
    ${LIB_SRCS}
)

# Set the include directories for the library.
# 'PUBLIC' means anyone linking to MyPackageLib will also get this include directory.
target_include_directories(MyPackageLib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Enable some basic warnings
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(MyPackageLib PRIVATE -Wall -Wextra -Wpedantic)
endif()

# --- Executable Target ---
add_executable(MyPackageApp src/main.cpp)
target_link_libraries(MyPackageApp PRIVATE MyPackageLib)

# --- Amalgamation Custom Target ---
# Generate a single header and single cpp file using the python script
find_package(Python3 COMPONENTS Interpreter REQUIRED)

set(AMALGAMATED_H "${CMAKE_CURRENT_SOURCE_DIR}/dist/mypackage_single.h")
set(AMALGAMATED_CPP "${CMAKE_CURRENT_SOURCE_DIR}/dist/mypackage_single.cpp")

# Define input files for the script
# We pass the automatically discovered headers and sources.
set(H_SRCS ${LIB_HDRS})
set(CPP_SRCS ${LIB_SRCS})
set(INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/include")

add_custom_target(amalgamate
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/amalgamate.py
        --h_out ${AMALGAMATED_H}
        --cpp_out ${AMALGAMATED_CPP}
        --h_src ${H_SRCS}
        --cpp_src ${CPP_SRCS}
        --include_dirs ${INCLUDE_DIRS}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Amalgamating files into single .h and .cpp package"
    VERBATIM
)
