import asyncio
from enum import Enum
from wizwalker import ClientHandler, Client, Keycode
from wizwalker.memory.memory_objects import DynamicWindow
from wizwalker.hotkey import Hotkey, Listener, ModifierKeys, HotkeyListener
from typing import List
import keyboard


class ActionButton(Enum):
    DELETE = "btnDelete"
    NEW = "btnNew"
    NEXT = "NextButton"
    SKIP = "SkipButton"
    OK = "OKButton"
    DONE = "DoneButton"


class GenderButton(Enum):
    GIRL = "GirlButton"
    BOY = "BoyButton"


class SchoolButton(Enum):
    STORM = "SelectStormButton"
    MYTH = "SelectMythButton"
    LIFE = "SelectLifeButton"
    FIRE = "SelectFireButton"
    ICE = "SelectIceButton"
    BALANCE = "SelectBalanceButton"
    DEATH = "SelectDeathButton"


class Macro(object):
    def __init__(self, handler: ClientHandler) -> None:
        self.handler = handler
        self.client = self.handler.get_new_clients()[0]
        self.macro_listner = HotkeyListener()

    def spawn_macro(self) -> None:
        asyncio.run(self.run_macro())

    async def run_macro(self):
        try:
            await self.client.mouse_handler.activate_mouseless()
            await self.client.hook_handler.activate_root_window_hook()
            await self.client.hook_handler.activate_render_context_hook()
            self.macro_listner.start()
            while True:
                await asyncio.sleep(1)
        finally:
            await self.handler.close()

    async def execute_character_macro(self, school: SchoolButton, gender: GenderButton):
        print("Executing macro")
        mouse_handler = self.client.mouse_handler
        await mouse_handler.click_window_with_name(ActionButton.DELETE)
        keyboard.write("abracadabra")
        dtl: List[DynamicWindow] = await self.client.root_window.get_windows_with_name(
            ActionButton.DELETE
        )
        await mouse_handler.click_window(dtl[1])
        await asyncio.sleep(0.1)
        await mouse_handler.click_window_with_name(ActionButton.NEW)
        for _ in range(11):
            await mouse_handler.click_window_with_name(ActionButton.NEXT)
            await asyncio.sleep(0.1)
        await mouse_handler.click_window_with_name(ActionButton.SKIP)
        await mouse_handler.click_window_with_name(school)
        await mouse_handler.click_window_with_name(ActionButton.OK)
        await mouse_handler.click_window_with_name(ActionButton.NEXT)
        girl: DynamicWindow = (
            await self.client.root_window.get_windows_with_name(gender)
        )[0]
        girl_box = await girl.scale_to_client()
        gx, gy = girl_box.center()
        gy_len = int((girl_box.y2 - girl_box.y1) / 2)
        await mouse_handler.click(gx, gy - gy_len)
        next: DynamicWindow = (
            await self.client.root_window.get_windows_with_name(ActionButton.NEXT)
        )[0]
        next_box = await next.scale_to_client()
        nx, _ = next_box.center()
        await mouse_handler.click(nx, gy - gy_len)
        await mouse_handler.click_window_with_name(ActionButton.NEXT)
        await asyncio.sleep(0.5)
        await mouse_handler.click_window_with_name(ActionButton.DONE)
