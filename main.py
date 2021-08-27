import PySimpleGUI as sg
from pynput import mouse
import time
from collections import deque
import tinydb
import os
import pygame


class MyException(Exception):
    pass


# ----------------  main loop  ----------------
class FidgetScroller:
    def __init__(self, speed_density=0.1, speed_list_size=4):
        self.speed_density = speed_density
        self.speed_density_ns = self.speed_density * 1_000_000_000
        self.speed_count = 0
        self.speed_max = 0
        self.speed_current = 0
        self.speed_current_avg = 0
        self.speed_last_messure = 0
        self.speed_list_size = speed_list_size
        self.speed_list_of_speeds = deque([0] * self.speed_list_size)
        self.all_ticks = 0

    def update_scroll(self):
        ltm = time.process_time_ns()
        if self.speed_last_messure + self.speed_density_ns < ltm:
            self.speed_last_messure = ltm
            self.speed_list_of_speeds.pop()
            calc = self.speed_count / self.speed_density
            self.speed_list_of_speeds.appendleft(calc)
            self.speed_current = calc
            self.speed_current_avg = (
                sum(self.speed_list_of_speeds) / self.speed_list_size
            )
            self.speed_count = 0
            self.speed_max = max([self.speed_max, self.speed_current])

    def main(self):
        ls = mouse.Listener(on_scroll=self._on_scroll)
        ls.start()

        # ----------------  Create Window  ----------------
        # sg.theme("DarkAmber")
        # sg.theme("DarkGrey12")
        # sg.theme("DarkBlue17")
        # sg.theme("DarkGrey3")
        layout_c1 = [
            [
                sg.Text(
                    "",
                    size=(12, 2),
                    font=("Helvetica", 12),
                    justification="left",
                    key="click_number",
                )
            ],
            [
                sg.Text(
                    "",
                    size=(12, 2),
                    font=("Helvetica", 12),
                    justification="left",
                    key="speed",
                )
            ],
            [
                sg.Text(
                    "",
                    size=(12, 2),
                    font=("Helvetica", 12),
                    justification="left",
                    key="max_speed",
                )
            ],
            [sg.Exit()],
        ]

        layout_c2 = [
            [
                sg.ProgressBar(
                    100,
                    orientation="v",
                    size=(12, 20),
                    key="-PROG_1-",
                    bar_color=(sg.theme_progress_bar_color()),
                )
            ]
        ]

        layout_c3 = [
            [
                sg.ProgressBar(
                    100,
                    orientation="v",
                    size=(12, 20),
                    key="-PROG_2-",
                    bar_color=(sg.theme_progress_bar_color()),
                )
            ]
        ]
        layout = [
            [
                sg.Column(layout_c1, element_justification="center"),
                sg.Column(layout_c2, element_justification="center"),
                sg.Column(layout_c3, element_justification="center"),
            ]
        ]


        layout_c4 = [[sg.TabGroup(
            [[
                sg.Tab(
                    'Tab1',
                    layout,
                    key='tab_1'),

                sg.Tab(
                    'Tab2',
                    [[]],
                    key='tab_2')
            ]],
            key='tabgroup',
            enable_events=True),
            sg.Graph((199, 200), (0, 0), (200, 200),
                    background_color='lightblue', key='-GRAPH-')
        ]]


        window = sg.Window(
            "Fidget Mouse Scroller!",
            layout_c4,
            auto_size_buttons=False,
            grab_anywhere=True,
            finalize=True
        )

        graph = window['-GRAPH-']           # type: sg.Graph
        print(graph.__dict__)
        embed = graph.TKCanvas
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # ----------------------------- PyGame Code -----------------------------
        # Call this function so the Pygame library can initialize itself
        pygame.init()
        screen = pygame.display.set_mode((200, 200))
        screen.fill(pygame.Color(255, 255, 255))

        pygame.display.init()
        pygame.display.update()

        # Set the title of the window
        # pygame.display.set_caption('Snake Example')

        while True:
            # --------- Read and update window --------
            event, values = window.read(timeout=0)

            # --------- Do Button Operations --------
            if event == sg.WIN_CLOSED or event == "Exit":
                break

            self.update_scroll()
            # --------- Display timer in window --------

            window["click_number"].update(f"Ticks\n{self.all_ticks/1000.0:02.03f} k")
            window["speed"].update(f"Current Speed\n{self.speed_current:03.0f} ticks/s")
            window["max_speed"].update(f"Max Speed\n{self.speed_max:03.0f} ticks/s")
            window["-PROG_1-"].update(self.speed_current, self.speed_max)
            window["-PROG_2-"].update(self.speed_current_avg, self.speed_max)
            # window["-PROG-"]._bar_color('red', sg.theme_background_color())

        # Broke out of main loop. Close the window.
        ls.stop()
        window.close()

    def _on_scroll(self, _x, _y, _dx, dy):
        self.speed_count += abs(dy)
        self.all_ticks += abs(dy)


fms = FidgetScroller()
fms.main()
