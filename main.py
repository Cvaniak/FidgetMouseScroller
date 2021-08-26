import PySimpleGUI as sg
from pynput import mouse
import sys
import time

arr = [0]*10
dist = 0

class MyException(Exception): pass
def on_click(*args):
    global dist
    dist += 1

def on_scroll(_x, _y, _dx, dy):
    global dist
    dist += abs(dy)
    print(time.time())
    print(dist)
    print(_x, _y, _dx, dy)

ls =  mouse.Listener(on_scroll=on_scroll, on_click=on_click)
ls.start()


# sg.theme('DarkAmber')   # Add a touch of color

# layout = [  [sg.Text('Some text on Row 1')],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')] ]

# window = sg.Window('Window Title', layout)
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel':
#         break
#     print('You entered ', values[0])

# window.close()
import PySimpleGUI as sg

# ----------------  Create Window  ----------------
# sg.theme('DarkAmber')   # Add a touch of color
layout_c = [[sg.Text('')],
          [sg.Text('', size=(8, 2), font=('Helvetica', 12), justification='left', key='click_number')],
          [sg.Text('', size=(8, 2), font=('Helvetica', 12), justification='left', key='speed')],
          [sg.Text('', size=(8, 2), font=('Helvetica', 12), justification='left', key='max_speed')],
          [sg.Exit(button_color=('white', 'firebrick4'))]]

layout = [[sg.Column(layout_c, element_justification='center')]]

window = sg.Window('Fidget Mouse Scroller!', layout,auto_size_buttons=False,
                   grab_anywhere=True)
#  no_titlebar=True,
# ----------------  main loop  ----------------
while (True):
    # --------- Read and update window --------
    event, values = window.read(timeout=0)

    # --------- Do Button Operations --------
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    try:
        interval = int(values['spin'])
    except:
        interval = 1

    # --------- Display timer in window --------

    window['click_number'].update(f'Scroll ticks {dist:02.0f}')

# Broke out of main loop. Close the window.
ls.stop()
window.close()