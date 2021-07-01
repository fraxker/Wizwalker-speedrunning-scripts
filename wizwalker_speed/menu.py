import asyncio
import tkinter as tk
from macro import SchoolButton, GenderButton, setup_loop
from config import WizConfig
from wizwalker import ClientHandler, ModifierKeys, Keycode
from typing import Union
from contextlib import suppress

class WizMenu(tk.Frame):
    def __init__(self) -> None:
        super().__init__()
        self.config = WizConfig()
        self.initUI()
        self.handler = ClientHandler()
        self.run_macro()

    def initUI(self) -> None:
        self.master.title("Wizard101 Speedrunning")
        menu = tk.Menu(self.master)
        menu.add_command(label="reset", command=self.open_macro_menu)
        self.master.config(menu=menu)

    def open_macro_menu(self) -> None:
        if self.macro_menu == None:
            self.macro_menu = MacroMenu()
        else:
            self.macro_menu.show()

    def run_macro(self):
        if self.event_loop == None:
            self.event_loop = asyncio.get_event_loop()
        if self.task is not None:
            self.task.cancel()
            with suppress(asyncio.CancelledError):
                self.event_loop.run_until_complete(self.task)
        self.task = asyncio.create_task(setup_loop(self.handler, *self.config.get_config()))

    def update_config(self, gender: GenderButton, school: SchoolButton, hotkey: Keycode, modifiers: Union[ModifierKeys, int]):
        self.config.set_config(school=school, gender=gender, key=hotkey, modifiers=modifiers)
        self.config.write()


class MacroMenu(object):
    def __init__(self, parent: WizMenu) -> None:
        self.__parent__ = parent
        self.ctl_bool = tk.BooleanVar(True)
        self.alt_bool = tk.BooleanVar(False)
        self.shift_bool = tk.BooleanVar(False)
        self.school_str = tk.StringVar(SchoolButton.STORM)
        self.gender_str = tk.StringVar(GenderButton.GIRL)
        self.initUI()

    def initUI(self) -> None:
        self.top = tk.Toplevel()
        self.top.title("Reset Macro Settings:")
        self.top.bind("<Key>", self.update_key)
        self.key: tk.Entry = tk.Entry(self.top, text="R", state=tk.DISABLED).grid(
            row=0, sticky=tk.W
        )
        tk.Checkbutton(self.top, text="Ctl", variable=self.ctl_bool).grid(
            row=1, sticky=tk.W
        )
        tk.Checkbutton(self.top, text="Alt", variable=self.alt_bool).grid(
            row=2, sticky=tk.W
        )
        tk.Checkbutton(self.top, text="Shift", variable=self.shift_bool).grid(
            row=3, sticky=tk.W
        )
        tk.OptionMenu(self.top, self.school_str, *[s for s in SchoolButton]).grid(
            row=4, sticky=tk.W
        )
        tk.OptionMenu(self.top, self.gender_str, *[g for g in GenderButton]).grid(
            row=5, sticky=tk.W
        )
        tk.Button(self.top, text="Close", command=self.close).grid(row=6, sticky=tk.W)
        tk.Button(self.top, text="Save", command=self.save).grid(row=7, sticky=tk.E)

    def close(self) -> None:
        self.top.withdraw()

    def save(self) -> None:
        modifiers = 0
        if self.ctl_bool.get():
            modifiers = ModifierKeys.CTRL | modifiers
        if self.alt_bool.get():
            modifiers = ModifierKeys.ALT | modifiers
        if self.shift_bool.get():
            modifiers = ModifierKeys.SHIFT | modifiers
        self.__parent__.update_config(GenderButton(self.gender_str.get()), SchoolButton(self.school_str.get()), Keycode(ord(self.key.get())), modifiers)
        self.__parent__.run_macro()
        self.close()

    def update_key(self, event: tk.Event):
        self.key.delete(0, "end")
        self.key.insert(0, event.char.upper())

    def show(self) -> None:
        self.top.update()
        self.top.deiconify()
