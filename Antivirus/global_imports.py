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

terminate = False
Scanned_Files = dict()


def terminate_and_delete(file_path,file_name,pid):
    print(str(file_path) + " maybe a malware")
    print("===========================================")
    try:
        os.kill(pid,signal.SIGTERM)
        shutil.copyfile(file_path,"./VirtualRecycle/" + str(file_name) + ".exe")
        Scanned_Files[file_path] = True
    except Exception as e:
        pass
    return True
