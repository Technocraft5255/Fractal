import pygame.locals
import threading
import sys
import time
from PIL import Image
import ctypes


screen_width, screen_height = 1920, 1080

_exit = False

julia_dll = ctypes.CDLL("./build/julia.dll")
julia_set_generator = julia_dll.julia_set_generator
julia_set_generator.argtypes = [
    ctypes.c_double, # param : julia_param_real
    ctypes.c_double, # param : julia_param_imag
    ctypes.c_int,    # param : screen_width
    ctypes.c_int,    # param : screen_height
    ctypes.c_double, # param : world_x_min
    ctypes.c_double, # param : world_x_max
    ctypes.c_double, # param : world_y_min
    ctypes.c_double  # param : world_y_max
]
julia_set_generator.restype = ctypes.POINTER(ctypes.c_int * (screen_width * screen_height))


if '--val' in sys.argv:
    func_val = complex(sys.argv[sys.argv.index("--val") + 1])
else:
    func_val = complex(0.39)

if '--threads' in sys.argv:
    threads_num = int(sys.argv[sys.argv.index("--threads") + 1])
else:
    threads_num = 64

if '--hidden' in sys.argv:
    hidden = True
else:
    hidden = False

if '--image' in sys.argv:
    mode = "image"
    image_path = sys.argv[sys.argv.index("--image") + 1]
else:
    mode = "window"
    image_path = ""

if mode == "image":
    image = Image.new('RGB', (screen_width, screen_height), color='white')
else:
    pygame.init()
    pygame.display.set_caption("Fractal Generator by Technocraft5255")
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    window = pygame.display.set_mode((screen_width, screen_height), pygame.locals.FULLSCREEN)
    _exit = False
    window.fill((255, 255, 255))
    font = pygame.font.SysFont("Gothic A1 black", 50)
    
    image = None

# Starting julia set compute
start_time = time.time()

julia_result_table = julia_set_generator(func_val.real, func_val.imag, 1920, 1080, -2.0, 2.0, -9.0/8, 9.0/8)
print(julia_result_table.contents[0])
if mode == "image":
    for y in range(screen_height):
        for x in range(screen_width):
            color_value = julia_result_table.contents[y * screen_width + x]
            image.putpixel((x, y), (color_value, color_value, color_value))
else:
    for y in range(screen_height):
        for x in range(screen_width):
            
            color_value = julia_result_table.contents[y * screen_width + x]
            if color_value != -1:
                window.set_at((x, y), (color_value, color_value, 255))
            else:
                window.set_at((x, y), (0, 0, 0))

print(f"Time taken: {round(time.time() - start_time, 2)} seconds with {threads_num} threads")

# Save the image if the user wants to save it as an image
if mode == "image":
    image.save(f"{image_path}")
    pygame.quit()
    sys.exit()

# Display the window if the user wants to display it as a window
if not hidden: # Check if the user wants to hide the info and axes
    window.blit(font.render(f"Z²-{func_val.real}+{func_val.imag}i", True, (0, 0, 0)), (15, 15))
    pygame.draw.rect(window, (255, 0, 0), (0, window.get_height() / 2, window.get_width(), 1))
    pygame.draw.rect(window, (0, 255, 0), (window.get_width() / 2, 0, 1, window.get_height()))
    pygame.draw.rect(window, (255, 255, 0), (window.get_width() / 2, window.get_height() / 2, 1, 1))
    pygame.mouse.set_visible(False)

while not _exit:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _exit = True
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                _exit = True
                pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass

