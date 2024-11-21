import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "customtkinter",
        "json",
        "datetime",
        "subprocess",
        "shutil",
        "webbrowser",
        "random",
        "time",
        "PIL",
        "PIL._imagingtk",
        "PIL._tkinter_finder"
    ],
    "include_files": [
        ("function.py", "function.py"),
        ("ui.py", "ui.py"),
        ("themes.py", "themes.py"),
        ("controller.py", "controller.py"),
        ("misc/configuration.json", "misc/configuration.json"),
        ("saves", "saves"),
        ("images", "images") 
    ],
    "excludes": ["test", "distutils", "email", "http", "xml"],
    "build_exe": "dist/TimeMate"
}

base = "Win32GUI" if sys.platform == "win32" else None

exe = Executable(
    script="app.py",
    base=base,
    target_name="TimeMate.exe",
    icon="images/app_logo.png"
)

setup(
    name="TimeMate",
    version="1.0",
    description="TimeMate Application",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
