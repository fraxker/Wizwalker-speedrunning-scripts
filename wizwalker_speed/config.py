import json
import pathlib
from wizwalker import ModifierKeys, Keycode
from typing import Tuple

DEFAULT = {
    "School" : "Balance",
    "Gender" : "Girl",
    "Key" : Keycode.R.value,
    "Modifiers": ModifierKeys.CTRL.value
}

class WizConfig(object):
    def __init__(self) -> None:
        self.path = pathlib.Path("./wiz_config.json")
        self.read_config()

    def read_config(self) -> None:
        if not self.path.exists():
            self.config = DEFAULT
            self.write()
            
        else:
            with self.path.open() as f:
                self.config = json.load(f)
    
    def write(self) -> None:
        with self.path.open("w") as f:
            json.dump(self.config, f)

    def set_config(self, school: str = None, gender: str = None, key: int = None, modifiers: int = None) -> None:
        if school is not None and school != self.config["School"]:
            self.config["School"] = school

        if gender is not None and gender != self.config["Gender"]:
            self.config["Gender"] = gender

        if key is not None and key != self.config["Key"]:
            self.config["Key"] = key

        if modifiers is not None and modifiers != self.config["Modifiers"]:
            self.config["Modifiers"] = modifiers

    def get_config(self) -> Tuple[str, str, int, int]:
        return (self.config["School"], self.config["Gender"], self.config["Key"], self.config["Modifiers"])
