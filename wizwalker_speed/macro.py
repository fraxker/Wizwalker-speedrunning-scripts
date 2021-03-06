import asyncio
from enum import Enum
from wizwalker import ClientHandler
from wizwalker.memory.memory_objects import DynamicWindow
from wizwalker.hotkey import HotkeyListener
from typing import List
import win32com.client
import time

from wizwalker.mouse_handler import MouseHandler


class ActionButton(Enum):
    """
    Class for Action button names
    """

    # Delete Button
    DELETE = "btnDelete"
    # New Button
    NEW = "btnNew"
    # Next Button
    NEXT = "NextButton"
    # Skip Button
    SKIP = "SkipButton"
    # Ok Button
    OK = "OKButton"
    # Done Button
    DONE = "DoneButton"
    # Cancel Button
    CANCEL = "BackButton"


class GenderButton(Enum):
    """
    Class for gender creation names
    """

    # Girl Button
    GIRL = "Girl"
    # Boy Button
    BOY = "Boy"

    def button_name(self) -> str:
        """
        Returns the formated button name.

        Returns:
            str: Button name
        """
        return self.value + "Button"


class SchoolButton(Enum):
    """
    Class for school Button Creation
    """

    # Storm Button
    STORM = "Storm"
    # Myth Button
    MYTH = "Myth"
    # Life Button
    LIFE = "Life"
    # Fire Button
    FIRE = "Fire"
    # Fire Button
    ICE = "Fire"
    # Balance Button
    BALANCE = "Balance"
    # Death Button
    DEATH = "Death"

    def button_name(self) -> str:
        """
        Returns the formated button name.

        Returns:
            str: Button name
        """
        return "Select" + self.value + "Button"


class Macro(object):
    """
    Class for executing the Macro
    """

    def __init__(self, handler: ClientHandler) -> None:
        """
        Construct a macro object. THis is used to execute the macro.

        Args:
            handler (ClientHandler): The ClientHandler to use
        """
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
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.shell.AppActivate("WizardGraphicalClient")

    async def run_macro(self) -> None:
        """
        (Async) Starts the macro listner and runs until end
        """
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
        """
        (Async) Executes the character creation macro.

        Args:
            school (str): The school the execute on
            gender (str): The gender to execute on
        """
        print("Executing Macro")
        mouse_handler = self.client.mouse_handler
        try:
            school_btn = SchoolButton(school)
            gender_btn = GenderButton(gender)
            await mouse_handler.activate_mouseless()
            try:
                await mouse_handler.click_window_with_name(ActionButton.NEW.value)
                await asyncio.sleep(0.25)
                await mouse_handler.click_window_with_name(ActionButton.CANCEL.value)
                await asyncio.sleep(0.25)
            except:
                await self.delete_charcter(mouse_handler)
            finally:
                await self.create_character(mouse_handler, school_btn, gender_btn)
        except Exception as e:
            print(e)
        finally:
            await mouse_handler.deactivate_mouseless()

    async def create_character(
        self,
        mouse_handler: MouseHandler,
        school_btn: SchoolButton,
        gender_btn: GenderButton,
    ):
        await mouse_handler.click_window_with_name(ActionButton.NEW.value)
        await asyncio.sleep(0.5)
        while True:
            try:
                await mouse_handler.click_window_with_name(ActionButton.SKIP.value)
                await asyncio.sleep(0.1)
                break
            except:
                await mouse_handler.click_window_with_name(ActionButton.NEXT.value)
                await asyncio.sleep(0.1)
        await mouse_handler.click_window_with_name(school_btn.button_name())
        await asyncio.sleep(0.1)
        await mouse_handler.click_window_with_name(ActionButton.OK.value)
        await asyncio.sleep(0.1)
        await mouse_handler.click_window_with_name(ActionButton.NEXT.value)
        await asyncio.sleep(0.1)
        girl: DynamicWindow = (
            await self.client.root_window.get_windows_with_name(
                gender_btn.button_name()
            )
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

    async def delete_charcter(self, mouse_handler: MouseHandler):
        await mouse_handler.click_window_with_name(ActionButton.DELETE.value)
        await asyncio.sleep(0.1)
        self.shell.SendKeys("abracadabra")
        await asyncio.sleep(0.1)
        dtl: List[DynamicWindow] = await self.client.root_window.get_windows_with_name(
            ActionButton.DELETE.value
        )
        await mouse_handler.click_window(dtl[1])
        await asyncio.sleep(0.5)
