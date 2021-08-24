from pynput import mouse
import sys
import time

arr = [0]*10
dist = 0

class MyException(Exception): pass

def on_click(*args):
    if args[3]:
        raise MyException()

def on_scroll(_x, _y, _dx, dy):
    global dist
    dist += abs(dy)
    print(time.time())
    print(dist)

# Collect events until released
with mouse.Listener(on_scroll=on_scroll, on_click=on_click) as listener:
    try:
        listener.join()
    except MyException:
        sys.exit()
