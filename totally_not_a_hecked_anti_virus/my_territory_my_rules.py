import psutil
import pathlib
import re
import time
import keyboard
from threading import Thread,Lock
import string
import os
import signal
import shutil

Scanned_Python = dict()
Scanned_Exes = dict()

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
            if  "python" in process_info['name'] and len(process_info['cmdline']) > 1:
                process = psutil.Process(proc.pid)
                initial_directory = get_process_initial_directory(process)
                
                same_file = str(pathlib.Path(process_info['cmdline'][1])) == str(pathlib.Path(__file__).parts[-1])

                pid = proc.pid
                name = proc.name
                if initial_directory and not same_file:
                    python_scripts.append((process_info['cmdline'][1], initial_directory,pid))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return python_scripts

def get_running_exes():
    exes = []
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_info = proc.as_dict(attrs=['name', 'exe'])
            process = psutil.Process(proc.pid)
            if process_info['exe'] and not "SYSTEM" in proc.username() and proc.name() != "Discord.exe":
                pid = proc.pid
                name = proc.name()
                exes.append((proc.name(),process_info['exe'],pid))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return exes

def scan_file(file_path, file_name,pid):
    global Scanned_Python
    full_path = pathlib.Path(file_path).joinpath(file_name)

    if full_path in Scanned_Python:
        if Scanned_Python[full_path] == True:
            try:
                os.kill(pid,signal.SIGTERM)
            except Exception as e:
                pass
        return
    
    with open(full_path) as py_file:
        strings = ""
        for line in py_file: strings += line

        pattern = r"keyboard\.on_press||psutil||keyboard||msvcrt"
        if re.findall(pattern,strings):
            print(str(full_path) + " maybe a malware")
            try:
                os.kill(pid,signal.SIGTERM)
                shutil.copyfile(file_path,"./VirtualRecycle/hack" + str(pid) + ".exe")
                Scanned_Python[full_path] = True
            except Exception as e:
                pass
        else:
            Scanned_Python[full_path] = False
            
            

def strings(file_name,file_path,pid, min=4):
    global Scanned_Exes
    
    if file_path in Scanned_Exes:
        if Scanned_Exes[file_path] == True:
            try:
                os.kill(pid,signal.SIGTERM)
            except Exception as e:
                pass
        return


    strings = []
    if not os.path.exists(file_path):
        return False
    with open(file_path, errors="ignore") as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min and result in ["keyboard","pynput","mouse"]:
                print(file_path + " maybe a malware")
                try:
                    os.kill(pid,signal.SIGTERM)
                    shutil.copyfile(file_path,"./VirtualRecycle/hack" + str(pid) + ".exe")
                    Scanned_Exes[file_path] = True
                except Exception as e:
                    pass
                return True

            result = ""
        if len(result) >= min and result in ["keyboard","pynput","mouse"]:  # catch result at EOF
            print(file_path + " maybe a malware")
            try:
                os.kill(pid,signal.SIGTERM)
                shutil.copyfile(file_path,"./VirtualRecycle/hack" + str(pid) + ".exe")
                Scanned_Exes[file_path] = True
            except Exception as e:
                pass
            return True
    Scanned_Exes[file_path] = False
    return False

terminate = False    

def python_thread():
    global terminate
    while True:
        running_scripts = get_running_python_scripts()
        for [script_path, initial_directory,pid] in running_scripts:
            scan_file(initial_directory,script_path,pid)
        time.sleep(1)
        if terminate:
            return

def exe_thread():
    global terminate
    while True:
        exes = get_running_exes()
        for [file_name,file_path,pid] in exes:
            strings(file_name,file_path,pid)
        time.sleep(1)
        if terminate:
            return
python = Thread(target=python_thread)
exe = Thread(target=exe_thread)


python.start()
exe.start()

while str(input()) != "0":
    continue
terminate = True

python.join()
exe.join()
