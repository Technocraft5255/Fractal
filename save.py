def wait_computing_ended():
    global threads
    while True:
        if len([t for t in threads if t.is_alive()]) == 0:
            break


def show_px(x1, x2):
    global x_origin, y_origin
    for xpx in range(int(x1), int(x2)):
        for ypx in range(int(-y_origin), int(y_origin)):
            val = xpx + ypx 
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