#!/usr/bin/env python3
import tkinter as tk
import asyncio
from wizwalker_speed.menu import WizMenu

async def run_tk(root: tk.Tk, interval=0.1):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:
            root.update()
            await asyncio.sleep(interval)
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise

async def main():
    root = tk.Tk()
    menu = WizMenu(root)
    await run_tk(root)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
