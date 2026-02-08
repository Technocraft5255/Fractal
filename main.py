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


start_time = time.time()


def wait_computing_ended():
    global threads
    while True:
        if len([t for t in threads if t.is_alive()]) == 0:
            break


def show_px(x1, x2):
    global x_origin, y_origin
    for xpx in range(int(x1), int(x2)):
        for ypx in range(int(-y_origin), int(y_origin)):
            compute_z = complex(xpx / y_origin * (1 / zoom), ypx / y_origin * (1 / zoom))
            

            #val = julia_compute_c(compute_z_c, cxmath.Complex(func_val.real, func_val.imag))
            val = julia_compute(compute_z)
            if val != -1:
                if mode == "image":
                    image.putpixel((xpx + x_origin, ypx + y_origin), (val, val, 255))
                else:
                    window.fill((val, val, 255), ((xpx + x_origin, ypx + y_origin), (1, 1)))
            else:
                if mode == "image":
                    image.putpixel((xpx + x_origin, ypx + y_origin), (0, 0, 0))
                else:
                    window.fill((0, 0, 0), ((xpx + x_origin, ypx + y_origin), (1, 1)))


def julia_compute(a) -> int:
    global func_val
    temp_val = func_val
    for i in range(100):
        a = a ** 2 + temp_val
        if a.real > 10 ** 50 or a.imag > 10 ** 50:
            return min(i * 5, 255)
    return -1


threads = []
for i in range(threads_num):
    t = threading.Thread(target=show_px, args=(
        -x_origin + (x_origin / (threads_num / 2) * i),
        -x_origin + x_origin / (threads_num / 2) + (x_origin / (threads_num / 2) * i)
    ))
    t.start()
    threads.append(t)

wait_computing_ended()
print(f"Time taken: {round(time.time() - start_time, 2)} seconds with {threads_num} threads")

if mode != "image":
    if not hidden:
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
else:
    image.save(f"{image_path}")
