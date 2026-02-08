#include <stdio.h>
#include <stdlib.h>
#include <cxmath/cxmath.h>

#define DLLEXPORT __declspec(dllexport)
#define min(a, b) ((a) < (b) ? (a) : (b))

DLLEXPORT int julia_compute(Complex z, Complex julia_param){
    int iter = 0; 
    while (iter < 100){
        Complex z = c_add(c_square(z), julia_param);
        if (z.real > 10e10 || z.imag > 10e10){
            return min(iter, 255);
        }
        iter++;
    }
    return -1;
}

Vector2 screen_to_world(Vector2 px, int screen_width, int screen_height, Vector2 world_pos_min, Vector2 world_pos_max){
    Vector2 world_pos;
    world_pos.x = world_pos_min.x + (px.x / screen_width) * (world_pos_max.x - world_pos_min.x);
    world_pos.y = world_pos_min.y + (px.y / screen_height) * (world_pos_max.y - world_pos_min.y);
    return world_pos;
}

DLLEXPORT int* julia_set_generator( // Fuction that returns a pointer to a table of integers 
    double julia_param_real,        // representing the julia set values for each pixel of the screen
    double julia_param_imag, 
    int screen_width, 
    int screen_height,
    double world_x_min,
    double world_x_max,
    double world_y_min,
    double world_y_max/*,
    int SSAA_factor (Super Sampling Anti Aliasing disabled for now)*/
){
    int *value_table = (int*)malloc(screen_width * screen_height * sizeof(int));
    Complex julia_param = {julia_param_real, julia_param_imag};
    Vector2 world_pos_min = {world_x_min, world_y_min};
    Vector2 world_pos_max = {world_x_max, world_y_max};

    /* Repeat for each pixel of the screen, 
    compute the corresponding point in the complex plane and 
    compute the julia value for it, then store it in the value_table
    */
    for (int xpx = 0; xpx < screen_width; xpx++){
        for (int ypx = 0; ypx < screen_height; ypx++){
            Vector2 px = {xpx, ypx};
            Vector2 world_pos = screen_to_world(px, screen_width, screen_height, world_pos_min, world_pos_max);

            Complex z = {world_pos.x, world_pos.y};
            int val = julia_compute(z, julia_param);
            value_table[ypx * screen_width + xpx] = val;
        }
    }
    return value_table;
}