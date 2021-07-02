import asyncio
from asyncio.events import set_child_watcher
import tkinter as tk
from .macro import SchoolButton, GenderButton, Macro
from .config import WizConfig
from wizwalker import ClientHandler, ModifierKeys, Keycode, Hotkey
from typing import Union
import threading


class WizMenu(tk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.config = WizConfig()
        self.event_loop = None
        self.task = None
        self.macro_key = None
        self.macro_menu = None
        self.initUI()
        self.handler = ClientHandler()
        self.macro = Macro(self.handler)
        self.event_loop = asyncio.get_event_loop()
        threading.Thread(target=self.macro.spawn_macro).start()
        self.add_hotkey()

    def initUI(self) -> None:
        self.master.title("Wizard101 Speedrunning")
        menu = tk.Menu(self.master)
        menu.add_command(label="reset", command=self.open_macro_menu)
        self.master.config(menu=menu)

    def open_macro_menu(self) -> None:
        if self.macro_menu == None:
            self.macro_menu = MacroMenu(self)
        else:
            self.macro_menu.show()

    def add_hotkey(self):
        if self.macro_key is not None:
            task = asyncio.create_task(
                self.macro.macro_listner.remove_hotkey(
                    self.macro_key.keycode, modifiers=self.macro_key.modifiers
                )
            )
            asyncio.gather(task)
        school, gender, key, mods = self.config.get_config()
        self.macro_key = Hotkey(
            Keycode(key),
            lambda: self.macro.execute_character_macro(school, gender),
            modifiers=mods | ModifierKeys.NOREPEAT,
        )
        task = asyncio.create_task(
            self.macro.macro_listner.add_hotkey(
                self.macro_key.keycode,
                lambda: self.macro.execute_character_macro(school, gender),
                modifiers=mods | ModifierKeys.NOREPEAT,
            )
        )
        asyncio.gather(task)

    def update_config(
        self,
        gender: GenderButton,
        school: SchoolButton,
        hotkey: Keycode,
        modifiers: Union[ModifierKeys, int],
    ):
        self.config.set_config(
            school=school.value, gender=gender.value, key=hotkey.value, modifiers=modifiers.value
        )
        self.config.write()


class MacroMenu(object):
    def __init__(self, parent: WizMenu) -> None:
        self.__parent__ = parent
        school, gender, key, modifiers = self.__parent__.config.get_config()
        self.ctl_bool = tk.BooleanVar()
        if modifiers & ModifierKeys.CTRL == ModifierKeys.CTRL:
            self.ctl_bool.set(True)
        self.alt_bool = tk.BooleanVar()
        if modifiers & ModifierKeys.ALT == ModifierKeys.ALT:
            self.alt_bool.set(True)
        self.shift_bool = tk.BooleanVar()
        if modifiers & ModifierKeys.SHIFT == ModifierKeys.SHIFT:
            self.shift_bool.set(True)
        self.school_str = tk.StringVar()
        self.school_str.set(school)
        self.gender_str = tk.StringVar()
        self.gender_str.set(gender)
        self.key = chr(key)
        self.initUI()

    def initUI(self) -> None:
        self.top = tk.Toplevel()
        self.top.title("Reset Macro Settings:")
        self.key_entry: tk.Entry = tk.Entry(self.top, text=self.key, state=tk.DISABLED)
        self.key_entry.grid(
            row=0, sticky=tk.W
        )
        self.top.bind("<Key>", self.update_key)
        tk.Checkbutton(self.top, text="Ctl", variable=self.ctl_bool).grid(
            row=1, sticky=tk.W
        )
        tk.Checkbutton(self.top, text="Alt", variable=self.alt_bool).grid(
            row=2, sticky=tk.W
        )
        tk.Checkbutton(self.top, text="Shift", variable=self.shift_bool).grid(
            row=3, sticky=tk.W
        )
        tk.OptionMenu(self.top, self.school_str, *[s.value for s in SchoolButton]).grid(
            row=4, sticky=tk.W
        )
        tk.OptionMenu(self.top, self.gender_str, *[g.value for g in GenderButton]).grid(
            row=5, sticky=tk.W
        )
        tk.Button(self.top, text="Close", command=self.close).grid(row=6, sticky=tk.W)
        tk.Button(self.top, text="Save", command=self.save).grid(row=6, sticky=tk.E)

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
        self.__parent__.update_config(
            GenderButton(self.gender_str.get()),
            SchoolButton(self.school_str.get()),
            Keycode(ord(self.key)),
            modifiers,
        )
        self.__parent__.add_hotkey()
        self.close()

    def update_key(self, event: tk.Event):
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, event.char.upper())

    def show(self) -> None:
        self.top.update()
        self.top.deiconify()
