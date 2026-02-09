#include <stdio.h>
#include <stdlib.h>
#include <cxmath/cxmath.h>

#define DLLEXPORT __declspec(dllexport)
#define min(a, b) ((a) < (b) ? (a) : (b))
#define abs(x) ((x) < 0 ? -(x) : (x))

/*DLLEXPORT int julia_compute(Complex z, Complex julia_param){
    //printf("z before: %f + %fi\n", z.real, z.imag);
    for (int iter=0; iter < 10; iter++){
        Complex z = complex_add((Complex){z.real * z.real - z.imag * z.imag, 2 * z.real * z.imag}, (Complex){0.3, 0.5});
        //printf("z after : %f + %fi\n", z.real, z.imag);
        if (z.real > 10e50){
            return min(iter * 5, 255);
        }
    }
    return -1;
}*/

DLLEXPORT int julia_compute(double z_real, double z_imag, double julia_param_real, double julia_param_imag){
    double z_real_init = z_real;
    for (int iter=0; iter < 500; iter++){
        double z_2_real = z_real * z_real - z_imag * z_imag;
        double z_2_imag = 2 * z_real * z_imag;
        z_real = z_2_real + julia_param_real;
        z_imag = z_2_imag + julia_param_imag;
        if ((z_real > 1.0e150) || (z_imag > 1.0e150)){
            return min(iter * 5, 255);
        }
    }
    return -1;
}

DLLEXPORT Vector2 screen_to_world(Vector2 px, int screen_width, int screen_height, Vector2 world_pos_min, Vector2 world_pos_max){
    Vector2 world_pos;
    world_pos.x = world_pos_min.x + (px.x / screen_width) * (world_pos_max.x - world_pos_min.x);
    world_pos.y = world_pos_min.y + (px.y / screen_height) * (world_pos_max.y - world_pos_min.y);
    return world_pos;
}

DLLEXPORT int* julia_set_generator( // Function that returns a pointer to a table of integers 
    double julia_param_real,        // representing the julia set values for each pixel of the screen
    double julia_param_imag, 
    int screen_width, 
    int screen_height,
    double world_x_min,
    double world_x_max,
    double world_y_min,
    double world_y_max,
    int SSAA_factor //(Super Sampling Anti Aliasing)
){
    printf("Generating julia set with parameters: %f + %fi\n", julia_param_real, julia_param_imag);
    int *value_table = (int*)malloc(screen_width * screen_height * sizeof(int));
    Vector2 world_pos_min = {world_x_min, world_y_min};
    Vector2 world_pos_max = {world_x_max, world_y_max};
    double xdperpx = (world_x_max - world_x_min) / screen_width; // Distance in the world space that corresponds to one pixel
    double ydperpx = (world_y_max - world_y_min) / screen_height;

    /* Repeat for each pixel of the screen, 
    compute the corresponding point in the complex plane and 
    compute the julia value for it, then store it in the value_table
    */
    for (int xpx = 0; xpx < screen_width; xpx++){
        for (int ypx = 0; ypx < screen_height; ypx++){
            Vector2 px = {xpx, ypx};
            Vector2 world_pos = screen_to_world(px, screen_width, screen_height, world_pos_min, world_pos_max);
            int val = julia_compute(world_pos.x, world_pos.y, julia_param_real, julia_param_imag);
            //int val = (int)(xpx+ypx)/12;
            //printf("Pixel: (%d, %d) -> World: (%f, %f) -> Value: %d\n", xpx, ypx, world_pos.x, world_pos.y, val);
            value_table[ypx * screen_width + xpx] = val;
        }
    }
    return value_table;
}