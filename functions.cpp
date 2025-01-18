#include <iostream>
#include <ctime>
#include <string.h>

using namespace std;

extern "C"
{
    const char *date()
    {
        time_t timp;
        time(&timp);
        return ctime(&timp);
    }

    const char *identify_source_module(int index)
    {
        const char *result;

        // Check the index and determine the module and part
        if (index >= 0 && index <= 4)
        {
            result = "Information extracted from Module1 part1";
        }
        else if (index >= 5 && index <= 9)
        {
            result = "Information extracted from Module1 part2";
        }
        else if (index >= 10 && index <= 14)
        {
            result = "Information extracted from Module1 part3";
        }
        else if (index >= 15 && index <= 19)
        {
            result = "Information extracted from Module2 part1";
        }
        else if (index >= 20 && index <= 24)
        {
            result = "Information extracted from Module2 part2";
        }
        else if (index >= 25 && index <= 29)
        {
            result = "Information extracted from Module2 part3";
        }
        else if (index >= 30 && index <= 34)
        {
            result = "Information extracted from Module3 part1";
        }
        else if (index >= 35 && index <= 39)
        {
            result = "Information extracted from Module3 part2";
        }
        else if (index >= 40 && index <= 44)
        {
            result = "Information extracted from Module3 part3";
        }
        else if (index >= 45 && index <= 49)
        {
            result = "Information extracted from Module4 part1";
        }
        else if (index >= 50 && index <= 54)
        {
            result = "Information extracted from Module4 part2";
        }
        else if (index >= 55 && index <= 59)
        {
            result = "Information extracted from Module4 part3";
        }
        else if (index >= 60 && index <= 64)
        {
            result = "Information extracted from Module5 part1";
        }
        else if (index >= 65 && index <= 69)
        {
            result = "Information extracted from Module5 part2";
        }
        else if (index >= 70 && index <= 74)
        {
            result = "Information extracted from Module5 part3";
        }
        else if (index >= 75 && index <= 79)
        {
            result = "Information extracted from Module6 part1";
        }
        else if (index >= 80 && index <= 84)
        {
            result = "Information extracted from Module6 part2";
        }
        else if (index >= 85 && index <= 89)
        {
            result = "Information extracted from Module6 part3";
        }
        else if (index >= 90 && index <= 94)
        {
            result = "Information extracted from Module7 part1";
        }
        else if (index >= 95 && index <= 99)
        {
            result = "Information extracted from Module7 part2";
        }
        else if (index >= 100 && index <= 104)
        {
            result = "Information extracted from Module7 part3";
        }
        else if (index >= 105 && index <= 109)
        {
            result = "Information extracted from Module8 part1";
        }
        else if (index >= 110 && index <= 114)
        {
            result = "Information extracted from Module8 part2";
        }
        else if (index >= 115 && index <= 119)
        {
            result = "Information extracted from Module8 part3";
        }
        else if (index >= 120 && index <= 124)
        {
            result = "Information extracted from Module9 part1";
        }
        else if (index >= 125 && index <= 129)
        {
            result = "Information extracted from Module9 part2";
        }
        else if (index >= 130 && index <= 134)
        {
            result = "Information extracted from Module9 part3";
        }
        else if (index >= 135 && index <= 139)
        {
            result = "Information extracted from Module10 part1";
        }
        else if (index >= 140 && index <= 144)
        {
            result = "Information extracted from Module10 part2";
        }
        else if (index >= 145 && index <= 149)
        {
            result = "Information extracted from Module10 part3";
        }
        else if (index >= 150 && index <= 154)
        {
            result = "Information extracted from Module11 part1";
        }
        else if (index >= 155 && index <= 159)
        {
            result = "Information extracted from Module11 part2";
        }
        else if (index >= 160 && index <= 164)
        {
            result = "Information extracted from Module11 part3";
        }
        else if (index >= 165 && index <= 169)
        {
            result = "Information extracted from Module12 part1";
        }
        else if (index >= 170 && index <= 174)
        {
            result = "Information extracted from Module12 part2";
        }
        else if (index >= 175 && index <= 179)
        {
            result = "Information extracted from Module12 part3";
        }
        return result; // return the C-style string
    }
}
