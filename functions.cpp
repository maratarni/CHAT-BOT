#include <iostream>
#include <ctime>

using namespace std;

extern "C" {
void date()
    {
        time_t timp;
        time(&timp);
        cout << "Today is " << ctime(&timp); // aici afisez data
        // pana aici am facut la laborator si am  ales sa pastrez partea asta
}
}
