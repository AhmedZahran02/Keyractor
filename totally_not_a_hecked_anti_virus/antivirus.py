from global_imports import *
from exe_scanner import exe_main
from python_scanner import python_main
import global_imports

global_imports.terminate = False    

python = Thread(target=exe_main)
exe = Thread(target=python_main)


python.start()
exe.start()

while str(input()) != "0":
    continue

global_imports.terminate = True

python.join()
exe.join()
