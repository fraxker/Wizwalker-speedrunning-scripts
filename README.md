# Wizwalker-speedrunning-scripts

This repository for the Wizard101 speedrunning tools. 

## Tools

### Macro
This tool is used to macro the deletion and creation of characters. Setting for school, gender, hotkey and modifcation keys can be found in the `wiz_config.json` file.

#### School
* Balance
* Life
* Storm
* Ice
* Fire
* Death
* Myth

#### Gender
* Boy
* Girl

#### Hotkey
Please refer to [this](https://github.com/StarrFox/wizwalker/blob/master/wizwalker/constants.py#L33) file for a full list of hotkey possibilities

#### Modifier Keys
Please refer to [this](https://github.com/StarrFox/wizwalker/blob/master/wizwalker/hotkey.py#L102) for a full list of modifier keys


## Installing
Everything can be installed by cloning the repo and running
`pip install .`

## Building
`pyinstaller --onefile ./main.py`

## Future Plans
* Stat Tracking
* Convert to winapi for key input
* Configuration GUI
