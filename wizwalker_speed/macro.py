import asyncio
from enum import Enum
from wizwalker import ClientHandler, Client, Keycode
from wizwalker.memory.memory_objects import DynamicWindow
from wizwalker.hotkey import Hotkey, Listener, ModifierKeys, HotkeyListener
from typing import List
import keyboard
import time


class ActionButton(Enum):
    DELETE = "btnDelete"
    NEW = "btnNew"
    NEXT = "NextButton"
    SKIP = "SkipButton"
    OK = "OKButton"
    DONE = "DoneButton"


class GenderButton(Enum):
    GIRL = "Girl"
    BOY = "Boy"

    def button_name(self) -> str:
        return self.value + "Button"


class SchoolButton(Enum):
    STORM = "Storm"
    MYTH = "Myth"
    LIFE = "LifeButton"
    FIRE = "Fire"
    ICE = "Ice"
    BALANCE = "Balance"
    DEATH = "Death"

    def button_name(self) -> str:
        return "Select" + self.value + "Button"


class Macro(object):
    def __init__(self, handler: ClientHandler) -> None:
        self.handler = handler
        while True:
            try:
                self.client = self.handler.get_new_clients()[0]
                break
            except IndexError as a:
                print("Waiting for client to open")
                time.sleep(5)
                continue
        self.macro_listener = HotkeyListener()

    async def run_macro(self):
        try:
            print("Activating Hooks")
            await self.client.hook_handler.activate_root_window_hook()
            await self.client.hook_handler.activate_render_context_hook()
            print("Starting listener")
            self.macro_listener.start()
            while True:
                await asyncio.sleep(1)
        finally:
            await self.handler.close()

    async def execute_character_macro(self, school: str, gender: str):
        print("Executing Macro")
        mouse_handler = self.client.mouse_handler
        try:
            school_btn = SchoolButton(school)
            gender_btn = GenderButton(gender)
            await mouse_handler.activate_mouseless()
            await mouse_handler.click_window_with_name(ActionButton.DELETE.value)
            await asyncio.sleep(0.1)
            keyboard.write("abracadabra")
            await asyncio.sleep(0.1)
            dtl: List[
                DynamicWindow
            ] = await self.client.root_window.get_windows_with_name(ActionButton.DELETE.value)
            await mouse_handler.click_window(dtl[1])
            await asyncio.sleep(0.5)
            await mouse_handler.click_window_with_name(ActionButton.NEW.value)
            await asyncio.sleep(0.1)

            try:
                await mouse_handler.click_window_with_name(ActionButton.NEXT.value)
            except:
                await mouse_handler.click_window_with_name(ActionButton.NEW.value)
                await asyncio.sleep(0.1)
                await mouse_handler.click_window_with_name(ActionButton.NEXT.value)

            for _ in range(10):
                await mouse_handler.click_window_with_name(ActionButton.NEXT.value)
                await asyncio.sleep(0.1)

            await mouse_handler.click_window_with_name(ActionButton.SKIP.value)
            await mouse_handler.click_window_with_name(school_btn.button_name())
            await mouse_handler.click_window_with_name(ActionButton.OK.value)
            await mouse_handler.click_window_with_name(ActionButton.NEXT.value)
            await asyncio.sleep(0.1)
            girl: DynamicWindow = (
                await self.client.root_window.get_windows_with_name(gender_btn.button_name())
            )[0]
            girl_box = await girl.scale_to_client()
            gx, gy = girl_box.center()
            gy_len = int((girl_box.y2 - girl_box.y1) / 2)
            await mouse_handler.click(gx, gy - gy_len)
            await asyncio.sleep(0.1)
            next: DynamicWindow = (
                await self.client.root_window.get_windows_with_name(ActionButton.NEXT.value)
            )[0]
            next_box = await next.scale_to_client()
            nx, _ = next_box.center()
            await mouse_handler.click(nx, gy - gy_len)
            await asyncio.sleep(0.1)
            await mouse_handler.click_window_with_name(ActionButton.NEXT.value)
            await asyncio.sleep(0.5)
            await mouse_handler.click_window_with_name(ActionButton.DONE.value)
        except Exception as e:
            print(e)
        finally:
            await mouse_handler.deactivate_mouseless()
