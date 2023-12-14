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
    name = "A",
    options = options,
    version = "1.0",
    description = 'A',
    executables = executables
)