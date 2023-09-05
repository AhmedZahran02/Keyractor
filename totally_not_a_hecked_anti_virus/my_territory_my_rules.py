import psutil
import pathlib
import re

def get_process_initial_directory(process):
    try:
        return process.cwd()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def get_running_python_scripts():
    python_scripts = []
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            process_info = proc.as_dict(attrs=['name', 'cmdline'])
            if process_info['name'] == 'python.exe' and len(process_info['cmdline']) > 1:
                process = psutil.Process(proc.pid)
                initial_directory = get_process_initial_directory(process)

                same_file = str(pathlib.Path(process_info['cmdline'][1])) == str(pathlib.Path(__file__).parts[-1])

                if initial_directory and not same_file:
                    python_scripts.append((process_info['cmdline'][1], initial_directory))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return python_scripts


def scan_python_file(file_path, file_name):
    full_path = pathlib.Path(file_path).joinpath(file_name)
    #print(full_path)
    with open(full_path) as py_file:
        strings = ""
        for line in py_file: strings += line

        pattern = r"keyboard\.on_press"
        if re.findall(pattern,strings):
            print(str(full_path) + " made by osama...")
        else:
            print(str(full_path) + " is 100% secure :pepehappy:")
    


    

running_scripts = get_running_python_scripts()

for [script_path, initial_directory] in running_scripts:
    scan_python_file(initial_directory,script_path)