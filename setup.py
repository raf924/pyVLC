# -*- encoding: utf-8 -*-
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"include_msvcr":True,"include_files":["html","application.js"],"packages": ["core","web","library"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "pyVLC",
        version = "0.1",
        description = "VLC-backended media player sporting a fully customizable HTML5 interface",
        options = {"build_exe": build_exe_options},
        executables = [Executable("__init__.py", base=base, compress=False, targetName="pyVLC.exe", icon="python.ico")])
