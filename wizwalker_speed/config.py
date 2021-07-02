import json
import pathlib
from wizwalker import ModifierKeys, Keycode
from typing import Tuple

# Default Dict to use if no file
DEFAULT = {
    "School": "Balance",
    "Gender": "Girl",
    "Key": Keycode.R.name,
    "Modifiers": ModifierKeys.CTRL.value,
}


class WizConfig(object):
    """
    Class for a configuration file. This is used as an interface instead of having to directly interact with the file itself.
    """

    def __init__(self) -> None:
        """
        Construct a new WizConfig object, looks for the config file and if not found creates one
        """
        self.path = pathlib.Path("./wiz_config.json")
        self.read_config()

    def read_config(self) -> None:
        """
        Reads the json config file. If not found creates one
        """
        if not self.path.exists():
            self.config = DEFAULT
            self.write()

        else:
            with self.path.open() as f:
                self.config = json.load(f)

    def write(self) -> None:
        """
        Writes the current dict to a config file
        """
        with self.path.open("w") as f:
            json.dump(self.config, f)

    def set_config(
        self,
        school: str = None,
        gender: str = None,
        key: str = None,
        modifiers: int = None,
    ) -> None:
        """
        Updates the data in the config file

        Args:
            school (str, optional): The school name to update. Defaults to None.
            gender (str, optional): The gender name to update. Defaults to None.
            key (str, optional): The key to update. Defaults to None.
            modifiers (int, optional): The modifier keys int to update. Defaults to None.
        """
        if school is not None and school != self.config["School"]:
            self.config["School"] = school

        if gender is not None and gender != self.config["Gender"]:
            self.config["Gender"] = gender

        if key is not None and key != self.config["Key"]:
            self.config["Key"] = key

        if modifiers is not None and modifiers != self.config["Modifiers"]:
            self.config["Modifiers"] = modifiers

    def get_config(self) -> Tuple[str, str, str, int]:
        """
        Gets the current config in form of a tuple.

        Returns:
            Tuple[str, str, str, int]: School, Gender, Key, Modifier Keys
        """
        return (
            self.config["School"],
            self.config["Gender"],
            self.config["Key"],
            self.config["Modifiers"],
        )
