#http://cx-freeze.readthedocs.org/en/latest/distutils.html
import sys
from cx_Freeze import setup, Executable

setup(name = "guifoo",
      version = "0.1",
      description = "My GUI application!",
      executables = [Executable("helloworld.py", base=None)])
