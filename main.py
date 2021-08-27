import PySimpleGUI as sg
from pynput import mouse
import time
from collections import deque
import tinydb
import os


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

        def collapse(layout, key):
            """
            Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
            :param layout: The layout for the section
            :param key: Key used to make this seciton visible / invisible
            :return: A pinned column that can be placed directly into your layout
            :rtype: sg.pin
            """
            return sg.pin(sg.Column(layout, key=key, visible=False))

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
        layout_tab_1 = [
            [
                sg.Column(layout_c1, element_justification="center", key="col_1"),
                sg.Column(layout_c2, element_justification="center", key="col_2"),
                sg.Column(layout_c3, element_justification="center", key="col_3"),
            ]
        ]

        layout_tab_2 = [
            [
                collapse(
                    [
                        [
                            sg.Graph(
                                (300, 300),
                                (0, 0),
                                (300, 300),
                                background_color="lightblue",
                                key="-GRAPH-",
                                visible=True,
                            )
                        ]
                    ],
                    "-SEC1-",
                ),
            ],
            [
                sg.Button("Play", key="-PLAY-"),
            ],
        ]

        layout_c4 = [
            [
                sg.TabGroup(
                    [
                        [
                            sg.Tab("Stats", layout_tab_1, key="tab_1"),
                            sg.Tab(
                                "Game",
                                layout_tab_2,
                                key="tab_2",
                            ),
                        ]
                    ],
                    key="tabgroup",
                    enable_events=True,
                ),
            ]
        ]

        window = sg.Window(
            "Fidget Mouse Scroller!",
            layout_c4,
            grab_anywhere=True,
            finalize=True,
            resizable=True,
        )
        a = 1
        graph_size = window["-GRAPH-"].get_size()
        print(graph_size)
        opened1, opened2 = False, True

        while True:
            # --------- Read and update window --------
            event, values = window.read(timeout=0)

            # --------- Do Button Operations --------
            if event == sg.WIN_CLOSED or event == "Exit":
                break

            if values["tabgroup"] == "tab_2" and a == 1:
                opened1 = True
                window["-SEC1-"].update(visible=opened1)
                a = 0
                print("as")

            elif values["tabgroup"] == "tab_1" and a == 0:
                opened1 = False
                window["-SEC1-"].update(visible=opened1)
                a = 1
                print("asa")

            self.update_scroll()
            # --------- Display timer in window --------

            window["click_number"].update(f"Ticks\n{self.all_ticks/1000.0:02.03f} k")
            window["speed"].update(f"Current Speed\n{self.speed_current:03.0f} ticks/s")
            window["max_speed"].update(f"Max Speed\n{self.speed_max:03.0f} ticks/s")
            window["-PROG_1-"].update(self.speed_current, self.speed_max)
            window["-PROG_2-"].update(self.speed_current_avg, self.speed_max)
            # window.refresh()
            # window["-PROG-"]._bar_color('red', sg.theme_background_color())

        # Broke out of main loop. Close the window.
        ls.stop()
        window.close()

    def _on_scroll(self, _x, _y, _dx, dy):
        self.speed_count += abs(dy)
        self.all_ticks += abs(dy)


fms = FidgetScroller()
fms.main()
