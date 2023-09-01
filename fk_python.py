import os.path
import tempfile
from os import mkdir
from threading import Lock

from pynput import keyboard
from pynput import mouse

tmp = tempfile.gettempdir()
if not os.path.exists(os.path.join(tmp, "pkl")):
    mkdir(os.path.join(tmp, "pkl"))
currentID = 0
file = ...
lock = Lock()


class KeyObjectConst:
    """
    bit switches
    """
    bit_type = 31
    bit_mod = 30
    bit_numpad = 29
    """
    focus changer mod keys / mouse buttons
    """
    focus_keys = [keyboard.Key.tab]
    focus_mouse_buttons = [0]


class KeyObject(KeyObjectConst):
    """
    x = 00000000 00000000 00000000 00000000
    """

    def __init__(self):
        self.x = 65 | 66 << 8

    def toBytes(self):
        return self.x.to_bytes(4, "big")

    def fromBytes(self, f):
        self.x.from_bytes(f.read(4), "big")

    def fromKeyboard(self, key: keyboard.Key):
        self.x = 0
        self.x |= 1 << self.bit_type
        if isinstance(key, keyboard.KeyCode):
            self.x |= 0 << self.bit_mod
            if hasattr(key, 'vk') and 96 <= key.vk <= 105:
                # numpad keys , fk python
                self.x |= ord('0') + key.vk - 96
                self.x |= 1 << self.bit_numpad
            else:
                self.x |= ord(key.char)
                self.x |= 0 << self.bit_numpad
        else:
            self.x |= 1 << self.bit_mod
            i = 1
            for k in self.focus_keys:
                if k == key:
                    self.x |= i << 8
                    break
                i = i + 1

    def fromMouse(self, key: mouse.Button):
        self.x = 0
        self.x |= 0 << self.bit_type
        val = 255
        if key == mouse.Button.left:
            val = 0
        elif key == mouse.Button.right:
            val = 1
        elif key == mouse.Button.middle:
            val = 2
        self.x |= val

    def isKeyboardKey(self):
        return self.x & (1 << self.bit_type) != 0

    def isMouseKey(self):
        return not self.isKeyboardKey()

    def isCharKey(self):
        return self.isKeyboardKey() and self.x & (1 << self.bit_mod) == 0

    def isModKey(self):
        return self.isKeyboardKey() and not self.isCharKey()

    def isNumpad(self):
        return self.isKeyboardKey() and self.x & (1 << self.bit_numpad) == 1

    def getChar(self):
        if not self.isKeyboardKey():
            return -1
        return chr(self.x & 0x000000ff)

    def getMouseButton(self):
        if self.isKeyboardKey():
            return -1
        return self.x & 0x000000ff

    def isFocusChangerKey(self):
        if self.isMouseKey():
            return self.getMouseButton() in self.focus_mouse_buttons
        else:
            return (self.x & 0x000000ff << 8) != 0

    def print(self):
        if self.isKeyboardKey():
            if self.isCharKey():
                if self.isNumpad():
                    print("keyboard{type=char(numpad) , value=", self.getChar(), "}")
                else:
                    print("keyboard{type=char , value=", self.getChar(), "}")
            else:
                print("keyboard{type=mod , focus=", self.isFocusChangerKey(), "}")
        else:
            print("mouse{value=", self.getMouseButton(), ", focus=", self.isFocusChangerKey(), "}")


def openFile():
    global file
    file = open(os.path.join(tmp, "pkl", str("b" + str(currentID))), "wb")


def closeFile():
    global file
    file.close()


def writeToFile(x):
    if not type(x) is KeyObject:
        print("gimme KeyObject you stupid fk")
        return
    b = x.toBytes()
    global file
    lock.acquire()
    try:
        file.write(b)
    except:
        print("Error writing in file")

    lock.release()


def handleKey(x):
    r = KeyObject()
    r.fromKeyboard(x)
    r.print()
    # writeToFile(r)


def handleMouseKey(x, y, button, pressed):
    if not pressed:
        return
    r = KeyObject()
    r.fromMouse(button)
    r.print()


if __name__ == "__main__":
    print("Cache Dir : " + tmp)
    openFile()
    writeToFile(KeyObject())

    listener = keyboard.Listener(on_press=handleKey)
    listener.start()

    listener2 = mouse.Listener(on_click=handleMouseKey)
    listener2.start()

    # listener.join()
    # listener2.join()

    # write_in_file("why are we still here")
    # write_in_file("why are we still here")

    input()
