import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "includes": ["numpy.core._methods", "numpy.lib.format", "cffi", "codecs", "encodings"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Sword Dancer",
        version = "0.1",
        description = "A melee combat roguelike",
        options = {"build_exe": build_exe_options},
        executables = [Executable("swordDancer.py", base=base)])
