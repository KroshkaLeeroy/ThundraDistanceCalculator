import sys

import pyautogui
import keyboard
import tkinter as tk
from threading import Thread
import math


class Cal:
    def __init__(self):
        self.size = 0
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0
        self.m_distance = 0
        self.correction = 0
        self.pressed = False
        self.key_watcher = True
        self.key_watcher_start = False
        keyboard.hook(self.print_pressed_keys)

        self.tk_set_up()
        self.objects_set_up()

    def distance(self):
        sqrt = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.size = self.rc_0_1.get()
        if self.size != '':
            self.size = float(self.size)
            res = self.size / 157.50625
            return round((sqrt * res) + self.correction, 1)
        return 'Enter map scale!'

    def get_coords(self):
        x, y = pyautogui.position()
        return x, y

    def objects_set_up(self):
        self.rc_0_0 = tk.Label(self.window, text="Map scale:")
        self.rc_0_0.grid(row=0, column=0, sticky="w")
        self.rc_0_1 = tk.Entry(self.window, width=10)
        self.rc_0_1.grid(row=0, column=1)
        self.correction_text = tk.Label(self.window, text="Correction:")
        self.correction_text.grid(row=1, column=0, sticky="w")
        self.correction_entry = tk.Label(self.window, text=self.correction)
        self.correction_entry.grid(row=1, column=1, sticky="n")
        self.rc_1_0 = tk.Label(self.window, text="Fir. coord:")
        self.rc_1_0.grid(row=2, column=0, sticky="w")
        self.rc_1_1 = tk.Label(self.window, text=f"{self.x1} : {self.y1}")
        self.rc_1_1.grid(row=2, column=1, sticky="n")
        self.rc_2_0 = tk.Label(self.window, text="Sec. coord:")
        self.rc_2_0.grid(row=3, column=0, sticky="w")
        self.rc_2_1 = tk.Label(self.window, text=f"{self.x2} : {self.y2}")
        self.rc_2_1.grid(row=3, column=1, sticky="n")
        self.rc_3_0 = tk.Label(self.window, text="Distance:")
        self.rc_3_0.grid(row=4, column=0, sticky="w")
        self.rc_3_1 = tk.Label(self.window, text=f"{self.m_distance}")
        self.rc_3_1.grid(row=4, column=1, sticky="n")

        self.btn_clear_all = tk.Button(self.window, text="Clear", command=self.clear_all)
        self.btn_clear_all.grid(row=0, column=2, sticky="w")

        self.copy_paste = tk.Button(self.window, text="Copy", command=self.copy_paste_to_clipboard)
        self.copy_paste.grid(row=4, column=2, sticky="w")

    def clear_all(self):
        self.rc_1_1.config(text="0 : 0")
        self.rc_2_1.config(text="0 : 0")
        self.rc_3_1.config(text="0")
        self.correction_entry.config(text="0")
        self.rc_1_1.config(text="0 : 0")
        self.rc_2_1.config(text="0 : 0")
        self.rc_3_1.config(text="0")
        self.correction = 0

    def copy_paste_to_clipboard(self):
        if self.size != '':
            self.correction = round(self.size - self.m_distance, 1)
        self.correction_entry.config(text=self.correction)

    def tk_set_up(self):
        self.window = tk.Tk()
        self.window.title("Distance calculator")
        self.window.geometry("210x120")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)
        self.window.protocol("WM_DELETE_WINDOW", self.stop_all_processes)

    def print_pressed_keys(self, e):
        if e.event_type == 'down':
            if not self.pressed:
                if e.name == 'end':
                    self.pressed = True
                    self.x1, self.y1 = self.get_coords()
                    self.updater()


        elif e.event_type == 'up':
            if e.name == 'end':
                self.x2, self.y2 = self.get_coords()
                self.pressed = False
                self.m_distance = self.distance()
                self.updater()


    def stop_all_processes(self):
        self.window.destroy()
        sys.exit()

    def updater(self):
        self.rc_1_1.configure(text=f"{self.x1} : {self.y1}")
        self.rc_2_1.configure(text=f"{self.x2} : {self.y2}")
        self.rc_3_1.configure(text=f"{self.m_distance}")
        self.correction_entry.configure(text=f"{self.correction}")

    def start(self):
        Thread(target=lambda: keyboard.wait('end')).start()
        self.window.mainloop()


if __name__ == "__main__":
    c = Cal()
    c.start()