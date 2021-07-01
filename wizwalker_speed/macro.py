import asyncio
from enum import Enum
from wizwalker import ClientHandler, Client, Keycode
from wizwalker.memory.memory_objects import DynamicWindow
from wizwalker.hotkey import Hotkey, Listener, ModifierKeys
from typing import List
import keyboard
from typing import Union


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


async def setup_loop(
    handler: ClientHandler,
    school: SchoolButton,
    gender: GenderButton,
    hotkey: Keycode,
    modifiers: Union[ModifierKeys, int],
):
    client = handler.get_new_clients()[0]

    try:
        await client.mouse_handler.activate_mouseless()
        await client.hook_handler.activate_root_window_hook()
        await client.hook_handler.activate_render_context_hook()
        macro_hotkey = Hotkey(
            hotkey,
            execute_character_macro,
            client,
            school,
            gender,
            modifiers=modifiers | ModifierKeys.NOREPEAT,
        )
        macro_listner = Listener(macro_hotkey)
        while True:
            task = asyncio.create_task(macro_listner.listen()) 
    finally:
        await handler.close()


async def execute_character_macro(
    client: Client, school: SchoolButton, gender: GenderButton
):
    mouse_handler = client.mouse_handler
    await mouse_handler.click_window_with_name(ActionButton.DELETE)
    keyboard.write("abracadabra")
    dtl: List[DynamicWindow] = await client.root_window.get_windows_with_name(
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
    girl: DynamicWindow = (await client.root_window.get_windows_with_name(gender))[0]
    girl_box = await girl.scale_to_client()
    gx, gy = girl_box.center()
    gy_len = int((girl_box.y2 - girl_box.y1) / 2)
    await mouse_handler.click(gx, gy - gy_len)
    next: DynamicWindow = (
        await client.root_window.get_windows_with_name(ActionButton.NEXT)
    )[0]
    next_box = await next.scale_to_client()
    nx, _ = next_box.center()
    await mouse_handler.click(nx, gy - gy_len)
    await mouse_handler.click_window_with_name(ActionButton.NEXT)
    await asyncio.sleep(0.5)
    await mouse_handler.click_window_with_name(ActionButton.DONE)
