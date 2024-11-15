#include<iostream>
#include <pybind11/pybind11.h>
#include <ctime>

using namespace std;
using py = pybind11;

void date()
{
        time_t timp;
        time(&timp);
        cout << "this is the time : " << ctime(&timp); // aici afisez data
        // pana aici am facut la laborator si am  ales sa pastrez partea asta
}

PYBIND11_MODULE(my_function, handle)
{
handle.doc="This is the date";
handle.def("date", &date);
}
