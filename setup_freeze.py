import sys
from cx_Freeze import setup, Executable

build_exe_options = {'include_files': [
    'Letter_G_dg_35002.ico', 'keywords.txt', 'settings.txt', 'README.txt', 'chromedriver.exe']
                     }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exec_options = [Executable("g_searcher.py", base=base,
                           icon='Letter_G_dg_35002.ico',
                           copyright="Copyright (C) 2018",
                           shortcutDir='DesktopFolder',
                           shortcutName='g_searcher',
                           )]

setup(name="Google search mailer",
      version="1.2",
      description="Google search mailer",
      options={"build_exe": build_exe_options},
      executables=exec_options,
      author='Pavlo Beliaev',
      author_email='a.agency@ukr.net')