import threading
import sys
import time
from PIL import Image

zoom = 2 / 3
width, height = 1920, 1080
x_origin, y_origin = width // 2, height // 2
func_val = complex(sys.argv[1])
start_time = time.time()
img = Image.new('RGB', (width, height), color='white')


def test_if_finished():
    global threads
    while True:
        if len([t for t in threads if t.is_alive()]) == 0:
            break


def show_px(x1, x2):
    global x_origin, y_origin
    for xpx in range(int(x1), int(x2)):
        for ypx in range(int(-y_origin), int(y_origin)):
            val = test_suite((xpx / y_origin * (1 / zoom) + ypx / y_origin * 1j * (1 / zoom)))
            if val != -1:
                img.putpixel((xpx + x_origin, ypx + y_origin), (val, val, 255))
            else:
                img.putpixel((xpx + x_origin, ypx + y_origin), (0, 0, 0))


def test_suite(a) -> int:
    global func_val
    temp_val = func_val
    for i in range(100):
        a = a ** 2 + temp_val
        if a.real > 10 ** 50 or a.imag > 10 ** 50:
            return min(i * 5, 255)
    return -1


threads_num = int(sys.argv[2])
threads = []
for i in range(threads_num):
    t = threading.Thread(target=show_px, args=(
        -x_origin + (x_origin / (threads_num / 2) * i),
        -x_origin + x_origin / (threads_num / 2) + (x_origin / (threads_num / 2) * i)
    ))
    t.start()
    threads.append(t)

test_if_finished()
img.save(f"{sys.argv[3]}")
print(f"Time taken: {round(time.time() - start_time, 2)} seconds with {threads_num} threads")
