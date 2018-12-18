cmake_minimum_required(VERSION 3.5)
project(Generators)

include("GenerateStuff.cmake")

add_generated_stuff(Interfaces interfaces.txt)

add_executable(main main.cpp)
target_link_libraries(main PRIVATE Interfaces)
