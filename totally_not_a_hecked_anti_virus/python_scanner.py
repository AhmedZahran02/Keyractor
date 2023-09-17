from global_imports import *
import global_imports

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
            # if the name of the process is python and has more than one command line argument
            if "python" in process_info['name'] and len(process_info['cmdline']) > 1:
                process = psutil.Process(proc.pid) #reference to the process
                initial_directory = get_process_initial_directory(process) # where this process was initialized
                
                # check if this process is the current one already
                same_file = str(initial_directory) == os.getcwd()
                pid = proc.pid
                name = proc.name
                if initial_directory and not same_file:
                    python_scripts.append((process_info['cmdline'][1], initial_directory,pid))
        except (Exception):
            pass
    return python_scripts


def scan_file(file_path, file_name,pid):
    global Scanned_Files

    full_path = pathlib.Path(file_path).joinpath(file_name)

    # if it was already scanned before then no need to scan it again just stop it
    if full_path in Scanned_Files:
        if Scanned_Files[full_path] == True:
            try:
                os.kill(pid,signal.SIGTERM)
            except Exception as e:
                pass
        return
    
    print("DEBUG: PYTHON SCANNING: " + full_path)

    with open(full_path) as py_file:
        strings = ""
        for line in py_file: strings += line

        pattern = r"keyboard\.on_press||psutil||pynput||msvcrt||listener.start()||pyperclip"

        if re.findall(pattern,strings):
            terminate_and_delete(full_path,file_name,pid)
            Scanned_Files[full_path] = True
        else:
            Scanned_Files[full_path] = False
   

def python_main():
    while not global_imports.terminate:

        running_scripts = get_running_python_scripts()

        for [script_path, initial_directory,pid] in running_scripts:
            scan_file(initial_directory,script_path,pid)

        time.sleep(1)

