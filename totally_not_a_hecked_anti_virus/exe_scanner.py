from global_imports import *
import global_imports

def get_running_exes():
    exes = []
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_info = proc.as_dict(attrs=['name', 'exe'])
            process = psutil.Process(proc.pid)
            # don't scan the processes made by the system doesn't make sense
            if process_info['exe'] and not "SYSTEM" in proc.username():
                exes.append((proc.name(),process_info['exe'],proc.pid))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return exes



def scan_exe_file(file_name,file_path,pid, min=4):
    global Scanned_Files
    
    # some sanity checks
    if not os.path.exists(file_path):
        return False

    # if the file was already scanned don't scan again
    if file_path in Scanned_Files:
        return

    print("DEBUG: SCANNING: " + file_path)
    
    def scan_result(result):
        if len(result) >= min and result in ["pynput","listener.start()","pyperclip","psutil","msvcrt","listener.start()"]:
            terminate_and_delete(file_path,file_name,pid)
            print("====================== found some sauce =============================")
            print(result)
            print("=====================================================================")
            Scanned_Files[file_path] = True
            return True
        return False

    with open(file_path, errors="ignore") as f:
        
        result = ""
        
        for c in f.read():
            
            if c in string.printable:
                result += c
                continue

            if scan_result(result): 
                
                return

            result = ""

        if not scan_result(result): Scanned_Files[file_path] = False


def exe_main():
    global_imports.terminate
    while not global_imports.terminate:
        exes = get_running_exes()

        for [file_name,file_path,pid] in exes:
            scan_exe_file(file_name,file_path,pid)

        time.sleep(1)