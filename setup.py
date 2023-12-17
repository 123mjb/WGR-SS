from cx_Freeze import setup, Executable

base = None    

executables = [Executable("game.py", base=base)]

packages = ["idna","pygame","random","math","json"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "B",
    options = options,
    version = "2.0",
    description = 'B',
    executables = executables
)