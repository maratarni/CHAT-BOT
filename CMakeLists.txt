cmake_minimum_required(VERSION 3.12)
project(my_function)
add_subdirectory(pybind11)
pybind11_add_module(my_function my_function.cpp)
