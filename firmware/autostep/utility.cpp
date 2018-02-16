#include "utility.h"
#define _USE_MATH_DEFINES
#include <math.h>

float deg_to_rad(float deg)
{
    return (M_PI*deg)/180.0;
}


float rad_to_deg(float rad)
{
    return (180.0*rad)/M_PI;
}
