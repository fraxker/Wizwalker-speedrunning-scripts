#!/usr/bin/env python3
import tkinter as tk
import asyncio
from wizwalker import ClientHandler, Keycode
from wizwalker_speed.config import WizConfig
from wizwalker_speed.macro import Macro


async def main():
    """
    (Async) Main loop, reads config then sets up listener
    """
    handler = ClientHandler()
    config = WizConfig()
    school, gender, key, modifiers = config.get_config()
    macro = Macro(handler)
    await macro.macro_listener.add_hotkey(
        Keycode[key],
        lambda: macro.execute_character_macro(school, gender),
        modifiers=modifiers,
    )
    await macro.run_macro()


if __name__ == "__main__":
    asyncio.run(main())
