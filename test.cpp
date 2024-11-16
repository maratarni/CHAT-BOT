#include <iostream>
#include <ctime>
#include <string.h>

extern "C"
{
    int test(int a, int b)
    {
        return a + b;
    }

    const char *date()
    {
        time_t timp;
        time(&timp);
        return ctime(&timp);
    }
}
